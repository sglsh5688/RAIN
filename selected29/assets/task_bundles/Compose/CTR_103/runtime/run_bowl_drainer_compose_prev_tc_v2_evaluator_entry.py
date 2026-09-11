#!/usr/bin/env python3
"""V2: exact live masks for every active and previous-completion TC call.

The frozen V1 observer, policy actions, TC thresholds and transition logic are
reused unchanged. Only the previous-completion mask resolver's unconditional
zero-region-mask defect is corrected. Every inference payload is audited.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

import numpy as np

import run_bowl_drainer_compose_evaluator_entry as v1


PROTOCOL = "drainer_compose_prev_tc_exact_gt_v2"
CAMERAS = ("agentview", "robot0_eye_in_hand")


def patch_hash(array):
    return hashlib.sha256(np.ascontiguousarray(array, dtype=np.float32).tobytes()).hexdigest()


def camera_record(camera, source, raw, patch):
    pixels = int(0 if raw is None else np.count_nonzero(raw))
    nonzero = int(0 if patch is None else np.count_nonzero(patch))
    zero_reason = ("current_camera_not_visible_or_projectable" if raw is None else
                   "empty_live_camera_mask" if pixels == 0 else
                   "patch_downsampling_zero" if nonzero == 0 else None)
    return dict(camera=camera, source=source, projected_or_visible_pixels=pixels,
                patch_nonzero=nonzero, patch_sum=float(0. if patch is None else np.asarray(patch).sum()),
                expected_patch_sha256=None if patch is None else patch_hash(patch),
                unavailable_live_mask=raw is None, zero_mask_reason=zero_reason)


class InferenceMaskAudit:
    def __init__(self, gpu_worker, env, spec, bddl_path, image_size):
        self.worker, self.env, self.spec = gpu_worker, env, spec
        self.bddl_path, self.image_size = str(bddl_path), int(image_size)
        self.active_original = v1.strict.rollout._resolve_active_masks
        self.previous_original = v1.strict.rollout._resolve_prev_completion_patches
        self.place_original = v1.strict.rollout._compute_place_masks
        self.infer_original = gpu_worker.infer
        self.pending = None
        self.records = []
        self.conditions = [("grasp", spec["objects"][0]), ("release", spec["regions"][0]),
                           ("grasp", spec["objects"][1]), ("release", spec["regions"][1])]

    def context(self):
        context = v1._current_context
        if context is None or context["active_index"] is None:
            raise RuntimeError("TC mask context is missing its exact active action stage")
        return context

    def set_pending(self, role, index, patches, raws, sources):
        if self.pending is not None:
            raise RuntimeError("A prepared GT mask context was not consumed by an inference call")
        action, object_id = self.conditions[index]
        self.pending = dict(role=role, condition_index=index, action_type=action, object_id=object_id,
                            expected_patches=[np.asarray(value, dtype=np.float32).copy() for value in patches],
                            camera_masks=[camera_record(camera, source, raw, patch)
                                          for camera, source, raw, patch in zip(CAMERAS, sources, raws, patches)])

    def active_masks(self, env, condition, *args, **kwargs):
        result = self.active_original(env, condition, *args, **kwargs)
        key = (str(condition.action_type), str(condition.object_id))
        index = self.conditions.index(key)
        if index != self.context()["active_index"]:
            raise RuntimeError("Active TC mask context differs from the condition actually executed")
        sources = [str(result[-1]), "exact_current_simulator_active_wrist"]
        self.set_pending("active_action", index, [result[1], result[3]], [result[0], result[2]], sources)
        self.pending["forward_place_enabled"] = condition.action_type == "grasp" and condition.target_place_patches is not None
        return result

    def place_masks(self, env, source_episodes, source_cond, target_episode,
                    target_object_id, corrected_bids, patch_grid, image_size, bddl_path):
        if self.pending is None or self.pending["role"] != "active_action":
            raise RuntimeError("Forward destination mask is outside its active inference context")
        index = self.pending["condition_index"]
        if index % 2 or target_object_id != self.spec["regions"][index // 2]:
            raise RuntimeError("Forward conditioning requested the wrong stage's destination")
        result = self.place_original(env, source_episodes, source_cond, target_episode,
                                     target_object_id, corrected_bids, patch_grid, image_size, bddl_path)
        if any(source not in {"sim_region_poly", "none"} for source in result[4:]):
            raise RuntimeError("Forward destination conditioning used a stored or wrong-source mask")
        expected = [None if patch is None or float(np.asarray(patch).sum()) <= 0 else np.asarray(patch, dtype=np.float32).copy()
                    for patch in result[:2]]
        self.pending["expected_place_patches"] = expected
        self.pending["place_region"] = str(target_object_id)
        records = [camera_record(camera, source, raw, patch) for camera, source, raw, patch in
                   zip(CAMERAS, result[4:], result[2:4], result[:2])]
        for record, submitted in zip(records, expected):
            record["computed_patch_sha256"] = record["expected_patch_sha256"]
            record["expected_patch_sha256"] = None if submitted is None else patch_hash(submitted)
        self.pending["place_camera_masks"] = records
        return result

    def previous_masks(self, env, prev_episode, prev_oid, prev_action_type,
                       corrected_bids, patch_grid, num_patches):
        """Resolve the PREVIOUS mask, never substitute the current action's mask."""
        key = (str(prev_action_type), str(prev_oid))
        if key not in self.conditions:
            raise RuntimeError(f"Unknown previous-completion condition: {key}")
        index = self.conditions.index(key)
        active = int(self.context()["active_index"])
        if index != active - 1:
            raise RuntimeError(f"Previous TC stage {index} must immediately precede active stage {active}")
        binding = (prev_episode.get("objects") or {}).get(str(prev_oid), {})
        is_region = not bool(binding.get("segmentable", True))
        if is_region and (key[0] != "release" or prev_oid != self.spec["regions"][index // 2]
                          or binding.get("name") != prev_oid):
            raise RuntimeError("Previous release TC must select one exact native destination site")
        raws, patches, sources = [], [], []
        for camera in CAMERAS:
            if is_region:
                projected = v1.render_region_mask(env, Path(self.bddl_path), str(prev_oid), self.image_size, camera)
                raw = None if projected is None else np.ascontiguousarray(projected[:, ::-1])
                source = "exact_previous_native_site" if raw is not None else "exact_previous_native_site_unprojectable_in_current_camera"
            else:
                raw = v1.strict.rollout.sim_mask_for_object_id(env, prev_episode, prev_oid,
                                                              corrected_bids=corrected_bids,
                                                              camera_name=camera, action_type=prev_action_type)
                source = "exact_previous_object_segmentation" if raw is not None else "exact_previous_object_not_visible_in_current_camera"
            patch = np.zeros(num_patches, dtype=np.float32) if raw is None else v1.strict.rollout._mask_to_patches(raw, patch_grid)
            if np.asarray(patch).shape != (num_patches,):
                raise RuntimeError("Previous TC mask patches have the wrong shape")
            raws.append(raw)
            patches.append(patch)
            sources.append(source)
        self.set_pending("previous_completion", index, patches, raws, sources)
        return tuple(patches)

    def infer(self, *args, **kwargs):
        if args or self.pending is None:
            raise RuntimeError("An inference call lacks an audited GT mask producer")
        pending = self.pending
        self.pending = None
        expected_action_id = v1.strict.runtime.action_type_to_id(pending["action_type"])
        if int(np.asarray(kwargs["action_type"]).reshape(-1)[0]) != expected_action_id:
            raise RuntimeError("Submitted TC action type differs from its mask condition")
        for key, expected, record in zip(("masks", "wrist_masks"), pending["expected_patches"], pending["camera_masks"]):
            actual = np.asarray(kwargs[key], dtype=np.float32)
            if actual.shape != (1, len(expected)) or not np.array_equal(actual[0], expected):
                raise RuntimeError(f"Actual {key} sent to TC differs from its live GT mask context")
            record["submitted_patch_sha256"] = patch_hash(actual[0])
            record["submitted_equals_expected"] = True
        if pending.get("forward_place_enabled") and "expected_place_patches" not in pending:
            raise RuntimeError("Enabled forward destination conditioning lacks its exact GT producer")
        place_records = pending.get("place_camera_masks") or [camera_record(camera, "not_conditioned_by_this_inference", None, None) for camera in CAMERAS]
        if "place_camera_masks" not in pending:
            for record in place_records:
                record["zero_mask_reason"] = "not_requested_for_this_inference"
        for key, expected, record in zip(("target_place_mask", "target_place_mask_wrist"),
                                          pending.get("expected_place_patches", [None, None]), place_records):
            actual = kwargs.get(key)
            if expected is None:
                if actual is not None:
                    raise RuntimeError(f"Unexpected or stale {key} was submitted to inference")
                record["submitted_patch_sha256"] = None
            else:
                actual = np.asarray(actual, dtype=np.float32)
                if actual.shape != (1, len(expected)) or not np.array_equal(actual[0], expected):
                    raise RuntimeError(f"Actual {key} differs from its exact current-stage GT destination")
                record["submitted_patch_sha256"] = patch_hash(actual[0])
            record["submitted_equals_expected"] = True
        context = self.context()
        timeline = context["active_stage_audit"]
        if not timeline:
            raise RuntimeError("Inference ran before its active-stage audit was recorded")
        output = self.infer_original(**kwargs)
        self.records.append(dict(
            call_index=len(self.records), role=pending["role"], condition_index=pending["condition_index"],
            action_type=pending["action_type"], object_id=pending["object_id"],
            active_condition_index=int(context["active_index"]), control_step=int(timeline[-1]["control_step"]),
            camera_masks=pending["camera_masks"],
            forward_place_region=pending.get("place_region"), forward_place_camera_masks=place_records,
            task_completion_probability=float(output["task_comp_prob"][0]) if "task_comp_prob" in output else None,
            target_place_conditioning_supplied=kwargs.get("target_place_mask") is not None,
            exact_actual_inference_inputs_verified=True,
        ))
        return output

    def install(self):
        v1.strict.rollout._resolve_active_masks = self.active_masks
        v1.strict.rollout._resolve_prev_completion_patches = self.previous_masks
        v1.strict.rollout._compute_place_masks = self.place_masks
        self.worker.infer = self.infer

    def restore(self):
        v1.strict.rollout._resolve_active_masks = self.active_original
        v1.strict.rollout._resolve_prev_completion_patches = self.previous_original
        v1.strict.rollout._compute_place_masks = self.place_original
        self.worker.infer = self.infer_original

    def as_dict(self):
        previous = [row for row in self.records if row["role"] == "previous_completion"]
        releases = [row for row in previous if row["action_type"] == "release"]
        return dict(protocol=PROTOCOL, every_inference_payload_verified=True, calls=len(self.records),
                    forward_place_payloads_verified=True,
                    active_action_calls=len(self.records) - len(previous), previous_completion_calls=len(previous),
                    previous_release_native_region_calls=len(releases),
                    previous_and_active_contexts_separate=True,
                    unconditional_nonsegmentable_zero_mask_path_disabled=True,
                    live_unprojectable_camera_masks_may_be_zero_with_explicit_reason=True,
                    policy_action_output_modified=False, tc_probability_output_modified=False,
                    tc_threshold_and_switch_logic_modified=False,
                    records=self.records)


def v2_episode(gpu_worker, env, init_state, text_feat, episode_data, conditions, **kwargs):
    spec = v1.task_spec(str(kwargs["bddl_path"]))
    audit = InferenceMaskAudit(gpu_worker, env, spec, kwargs["bddl_path"], v1.strict.rollout.LIBERO_ENV_RESOLUTION)
    audit.install()
    try:
        frames, success, meta = v1.ordered_placement_episode(gpu_worker, env, init_state, text_feat,
                                                           episode_data, conditions, **kwargs)
    finally:
        audit.restore()
    if audit.pending is not None:
        raise RuntimeError("Episode left an unused TC mask context")
    evidence = audit.as_dict()
    if not evidence["calls"] or (success and not evidence["previous_release_native_region_calls"]):
        raise RuntimeError("Episode lacks required exact GT TC inference evidence")
    meta.update(drainer_gt_mask_protocol=PROTOCOL, drainer_tc_inference_masks=evidence,
                prior_v1_zero_previous_region_masks_fixed=True,
                policy_action_generation_modified=False, policy_tc_switching_modified=False)
    return frames, success, meta


v1.strict.evaluator.run_single_episode_libero_ex = v2_episode


if __name__ == "__main__":
    v1.strict.evaluator.main()
