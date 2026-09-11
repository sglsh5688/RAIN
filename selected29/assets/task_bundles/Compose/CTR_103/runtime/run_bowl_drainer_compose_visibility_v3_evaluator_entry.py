#!/usr/bin/env python3
"""V3: preserve a genuinely empty visible GT mask without disguising errors.

Only active grasp `sim_missing` is refined. Normal nonmissing results, previous
TC checks, wrist masks, action generation, transition logic and scoring are
unchanged. Empty means a successful current raw segmentation, an exact known
object binding, and zero pixels belonging to that object in that camera.
"""

from __future__ import annotations

import hashlib
import numpy as np

import run_bowl_drainer_compose_prev_tc_v2_evaluator_entry as v2

PROTOCOL = "drainer_compose_visible_empty_gt_v3"
v1 = v2.v1


def exact_object_geoms(env, episode, object_id, corrected_bids, action_type):
    obj = (episode.get("objects") or {}).get(str(object_id))
    if not obj or not obj.get("segmentable", True) or action_type != "grasp":
        raise RuntimeError("Visible-empty recovery requires a known segmentable grasp object")
    bids = list(corrected_bids.get(str(object_id), []))
    expected = obj.get("body_name", obj.get("name"))
    if (len(bids) != 1 or int(bids[0]) <= 0 or int(bids[0]) >= env.sim.model.nbody
            or env.sim.model.body_id2name(int(bids[0])) != expected):
        raise RuntimeError("Visible-empty recovery lacks its exact verified object body")
    bodies = {int(bids[0])}
    parents = np.asarray(env.sim.model.body_parentid)
    while True:
        expanded = bodies | {index for index, parent in enumerate(parents) if int(parent) in bodies}
        if expanded == bodies:
            break
        bodies = expanded
    belonging = np.flatnonzero(np.isin(env.sim.model.geom_bodyid, list(bodies)))
    runtime = v1.strict.runtime
    explicit = runtime._get_task_specific_geom_ids(env, episode, object_id, action_type=action_type)
    if not explicit:
        explicit = runtime.get_object_geom_ids(episode, object_id, action_type=action_type)
    geoms = np.asarray(explicit if explicit else belonging, dtype=np.int32)
    if not len(geoms) or not set(geoms.tolist()).issubset(set(belonging.tolist())):
        raise RuntimeError("Visible-empty recovery lacks exact object-owned segmentation geoms")
    return geoms, dict(body_id=int(bids[0]), body_name=expected,
                      geom_ids=geoms.tolist(), geom_names=[env.sim.model.geom_id2name(int(g)) for g in geoms])


class VisibleEmptyAudit:
    def __init__(self, env, original_active):
        self.env, self.original = env, original_active
        self.calls = 0
        self.empty = []

    def active_masks(self, env, condition, episode, corrected_bids, *args, **kwargs):
        ordinal = self.calls
        self.calls += 1
        rendered = {}
        errors = []
        original_render = env.sim.render

        def capture_render(*render_args, **render_kwargs):
            camera = render_kwargs.get("camera_name")
            try:
                result = original_render(*render_args, **render_kwargs)
            except Exception as exc:
                if render_kwargs.get("segmentation"):
                    errors.append(dict(camera=camera, type=type(exc).__name__, message=str(exc)))
                raise
            if render_kwargs.get("segmentation"):
                rendered.setdefault(camera, []).append(np.asarray(result))
            return result

        env.sim.render = capture_render
        try:
            result = self.original(env, condition, episode, corrected_bids, *args, **kwargs)
        finally:
            env.sim.render = original_render
        if str(result[-1]) != "sim_missing":
            return result  # Identity and all arrays are unchanged on existing paths.
        if errors:
            raise RuntimeError(f"Current GT segmentation renderer failed, not an empty mask: {errors}")
        if str(condition.action_type) != "grasp":
            raise RuntimeError("Only active grasp visibility can be classified as empty GT")
        frames = rendered.get("agentview", [])
        if len(frames) != 1:
            raise RuntimeError("Missing exactly one current agent segmentation render")
        seg = frames[0]
        if (seg.shape != (256, 256, 2) or not np.issubdtype(seg.dtype, np.integer)
                or not np.any(seg[..., 0] == 5)):
            raise RuntimeError("Malformed/empty-scene raw segmentation is not a valid invisible-object mask")
        geoms, binding = exact_object_geoms(env, episode, str(condition.object_id), corrected_bids,
                                           str(condition.action_type))
        raw = np.logical_and(seg[..., 0] == 5, np.isin(seg[..., 1], geoms)).astype(np.uint8)
        if np.count_nonzero(raw) or np.count_nonzero(result[1]):
            raise RuntimeError("sim_missing conflicts with visible exact object pixels or nonzero patches")
        context = v1._current_context
        if context is None or context["active_index"] not in (0, 2):
            raise RuntimeError("Empty GT recovery is outside the exact active pickup stage")
        self.empty.append(dict(active_call_index=ordinal, condition_index=int(context["active_index"]),
            object_id=str(condition.object_id), camera="agentview", binding=binding,
            raw_segmentation_render_succeeded=True, raw_segmentation_shape=list(seg.shape),
            raw_segmentation_dtype=str(seg.dtype), scene_geom_pixels=int(np.count_nonzero(seg[..., 0] == 5)),
            raw_segmentation_sha256=hashlib.sha256(seg.tobytes()).hexdigest(),
            exact_object_visible_pixels=0, patch_nonzero=0,
            classification="known_object_not_visible_in_current_camera",
            stored_mask_used=False, renderer_exception_suppressed=False,
            previous_tc_helper_modified=False, wrist_result_modified=False))
        fixed = list(result)
        fixed[0] = np.ascontiguousarray(raw[::-1, ::-1])
        fixed[-1] = "sim_seg"
        return tuple(fixed)

    def as_dict(self, meta):
        active = [row for row in meta["drainer_tc_inference_masks"]["records"] if row["role"] == "active_action"]
        if len(active) != self.calls:
            raise RuntimeError("Active availability calls do not match actual active inference calls")
        for record in self.empty:
            payload = active[record["active_call_index"]]
            camera = payload["camera_masks"][0]
            if (payload["condition_index"] != record["condition_index"]
                    or payload["object_id"] != record["object_id"]
                    or camera["source"] != "sim_seg" or camera["patch_nonzero"]
                    or camera["zero_mask_reason"] != "empty_live_camera_mask"):
                raise RuntimeError("Validated-empty GT differs from V2 actual inference proof")
            record.update(inference_call_index=payload["call_index"], control_step=payload["control_step"],
                          actual_inference_mask_sha256=camera["submitted_patch_sha256"])
        return dict(protocol=PROTOCOL, active_calls=self.calls,
                    nonmissing_calls_returned_unchanged=self.calls - len(self.empty),
                    validated_empty_agent_calls=len(self.empty), records=self.empty,
                    only_active_agent_missing_branch_recovered=True,
                    nonmissing_producer_results_returned_by_identity=True,
                    previous_tc_and_wrist_mask_helpers_unchanged=True,
                    action_generation_and_tc_switching_unchanged=True,
                    native_order_support_scoring_unchanged=True,
                    renderer_errors_and_invalid_bindings_are_not_empty_masks=True)


def visibility_episode(gpu_worker, env, init_state, text_feat, episode_data, conditions, **kwargs):
    original_active = v1.strict.rollout._resolve_active_masks
    availability = VisibleEmptyAudit(env, original_active)
    # Installed BEFORE V2 constructs InferenceMaskAudit, so the corrected raw
    # producer is inside V2's pending payload context, not outside it.
    v1.strict.rollout._resolve_active_masks = availability.active_masks
    try:
        frames, success, meta = v2.v2_episode(gpu_worker, env, init_state, text_feat,
                                            episode_data, conditions, **kwargs)
    finally:
        v1.strict.rollout._resolve_active_masks = original_active
    meta["drainer_mask_availability_protocol"] = PROTOCOL
    meta["drainer_visible_empty_gt_audit"] = availability.as_dict(meta)
    return frames, success, meta


v1.strict.evaluator.run_single_episode_libero_ex = visibility_episode


if __name__ == "__main__":
    v1.strict.evaluator.main()
