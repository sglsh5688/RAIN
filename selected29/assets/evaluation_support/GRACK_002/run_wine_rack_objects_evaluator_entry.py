#!/usr/bin/env python3
"""Native Goal rack masks/replay with released top-deck physical scoring.

Only process-local evaluation/observation adapters are changed. The frozen
RAIN action generation, task-completion switching and gripper controls remain
unchanged. Both target and destination use the original current body GT masks.
"""
from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path

import numpy as np

import run_diverse_adapt_evaluator_entry as exact
from cream_cheese_bowl_layout import apply_fixtures, position_error, state_hash
from novel_feedback_object_bindings import register_object_bindings
from novel_scene_common import sections, typed_declarations
from wine_rack_object_support import FIXTURE, SOURCE_SITE, SITE, TASKS, RackPlacementObserver, RackPlacementProbe, install_rack_adapt_geometry

PROTOCOL = "goal_wine_rack_native_body_mask_adapt_full_deck_released_v2"
register_object_bindings()
install_rack_adapt_geometry()
for _object in TASKS.values():
    exact.benchmark_support.ACTION_OBJECTS[_object] = dict(name=_object+"_main", body_name=_object+"_main",
        body_ids=[0], geom_ids=[], segmentable=True)
# Preserve the original learned rack binding, not a rendered surface/region.
exact.benchmark_support.ACTION_OBJECTS[SITE] = dict(name=FIXTURE+"_main", body_name=FIXTURE+"_main",
    body_ids=[0], geom_ids=[], segmentable=True)
_base_episode = exact.exact_episode
_active_task = None


def validate_episode_request(episode_data, conditions, kwargs):
    rules = kwargs.get("eval_rules") or {}
    task_id = rules.get("task_id")
    if task_id not in TASKS:
        raise RuntimeError("Only the three requested GRACK tasks are authorized by this entry")
    object_id = TASKS[task_id]
    if (rules.get("required_goal_atoms") != [f"on({object_id}, {SITE})"]
            or rules.get("custom_eval_needed") is not True
            or str(rules.get("category", "")).lower() != "adapt"
            or rules.get("forbidden_goal_atoms") or rules.get("continue_after_success")
            or rules.get("requires_transition") or rules.get("sequence_stages")
            or rules.get("final_tc_gate") is not False or rules.get("support_hold_control_steps") != 5
            or rules.get("no_gripper_contact_required") is not True
            or rules.get("exact_original_upper_deck_support_required") is not True
            or rules.get("native_goal_required") is not False
            or rules.get("legacy_native_on_auxiliary_only") is not True
            or rules.get("annotated_goal_required") is not True
            or rules.get("body_center_over_deck_required") is not True
            or rules.get("body_center_above_deck_required") is not True):
        raise RuntimeError("New full-deck On plus released exact top-deck support for five controls is required")
    if (kwargs.get("max_steps") != 520 or kwargs.get("dino_input_size", 224) != 224
            or kwargs.get("replan_steps", 8) != 8 or kwargs.get("num_inference_steps", 4) != 4
            or kwargs.get("feas_threshold", .7) != .7 or kwargs.get("consecutive_stop", 2) != 2):
        raise RuntimeError("Frozen 520-step RAIN action/TC settings differ")
    actions = [(str(c.action_type), str(c.object_id)) for c in conditions]
    if actions != [("grasp", object_id), ("release", SITE)]:
        raise RuntimeError("Only exact target grasp followed by the original rack release is allowed")
    objects = (episode_data or {}).get("objects", {})
    for identity, body in ((object_id, object_id+"_main"), (SITE, FIXTURE+"_main")):
        binding = objects.get(identity, {})
        if (binding.get("name") != body or binding.get("body_name", body) != body
                or binding.get("segmentable") is not True):
            raise RuntimeError("Wrong native target/rack body mask binding")
    bddl = sections(Path(kwargs["bddl_path"]).read_text())
    normalized = lambda value: [normalized(x) for x in value] if isinstance(value, list) else str(value).lower()
    if normalized(bddl.get(":goal", [])) != [["and", ["on", object_id, SITE]]]:
        raise RuntimeError("BDDL must contain exactly the selected new full-upper-deck rack goal")
    declarations = typed_declarations(bddl.get(":objects", []))
    if (declarations.get(object_id) != object_id.rsplit("_", 1)[0] or "wine_bottle_1" in declarations
            or set(TASKS.values()) & set(declarations) != {object_id}):
        raise RuntimeError("Exactly one native replacement target must replace the original wine bottle")
    fixtures = typed_declarations(bddl.get(":fixtures", []))
    if fixtures.get(FIXTURE) != "wine_rack":
        raise RuntimeError("The original native-size wine rack is required")
    return task_id, object_id, actions


def rack_episode(gpu_worker, env, init_state, text_feat, episode_data, conditions, **kwargs):
    global _active_task
    task_id, object_id, actions = validate_episode_request(episode_data, conditions, kwargs)
    if _active_task is not None:
        raise RuntimeError("One evaluator process may run only one rack episode at a time")
    replay_path = Path(kwargs["bddl_path"]).parent / "FIXTURE_REPLAY.json"
    replay = json.loads(replay_path.read_text())
    if replay.get("task_id") != task_id or len(replay.get("rows", [])) != 5:
        raise RuntimeError("Exactly five matching task-specific fixture replays are required")
    matches = [r for r in replay["rows"] if r["state_sha256"] == state_hash(init_state)]
    if len(matches) != 1:
        raise RuntimeError("Exactly one validated initial-state replay must match this episode")
    snapshot = matches[0]
    if not snapshot.get("fixture_model_poses") or not snapshot.get("settled_body_positions"):
        raise RuntimeError("Exact original fixture poses and settled-state reference are mandatory")
    observer = RackPlacementObserver(object_id)
    probe, tracker = None, None
    controls = fixture_calls = settling_controls = 0
    initial_errors, active_audit, inference_audit = [], [], []
    mask_sources = Counter()
    last_masks = None
    originals = {name: getattr(exact.rollout, name) for name in (
        "update_eval_tracker", "custom_eval_now", "custom_eval_success", "custom_eval_failed",
        "_resolve_active_masks", "_resolve_prev_completion_patches")}
    original_reset, original_set, original_step, original_infer = env.reset, env.set_init_state, env.step, gpu_worker.infer

    def reset(*args, **kw):
        nonlocal fixture_calls
        result = original_reset(*args, **kw)
        apply_fixtures(env, snapshot["fixture_model_poses"])
        fixture_calls += 1
        return result

    def set_state(state, *args, **kw):
        nonlocal fixture_calls
        if state_hash(state) != snapshot["state_sha256"]:
            raise RuntimeError("The runtime attempted to restore a different initial state")
        apply_fixtures(env, snapshot["fixture_model_poses"])
        fixture_calls += 1
        return original_set(state, *args, **kw)

    def observe(current, current_tracker, index):
        nonlocal probe
        originals["update_eval_tracker"](current, current_tracker, index)
        if probe is None:
            probe = RackPlacementProbe(current, object_id)
        facts = probe.snapshot()
        if bool(current.check_success()) != facts["annotated_on"]:
            raise RuntimeError("New BDDL success differs from the annotated full-deck On predicate")
        observer.update(index, facts)

    def step(*args, **kw):
        nonlocal controls, settling_controls
        result = original_step(*args, **kw)
        if tracker is None:
            settling_controls += 1
        else:
            controls += 1
            observe(env, tracker, controls)
        return result

    def update(current, current_tracker, step_idx):
        nonlocal tracker
        if tracker is None:
            if int(step_idx) != 0 or settling_controls != 10:
                raise RuntimeError("Pre-policy control zero must follow exactly ten settling controls")
            if (not current_tracker.get("custom") or current_tracker.get("category") != "ADAPT"
                    or current_tracker.get("continue_after_success")):
                raise RuntimeError("Native-success early termination must be disabled by custom Adapt scoring")
            error = position_error(current, snapshot["settled_body_positions"])
            if error > 1e-8:
                raise RuntimeError("The validated common layout or exact original fixed fixture replay changed")
            initial_errors.append(error)
            observe(current, current_tracker, 0)
            tracker = current_tracker
        elif current_tracker is not tracker or int(step_idx) != controls:
            raise RuntimeError("An actual policy or gripper control observation was skipped")

    def active_masks(current, condition, *args, **kw):
        nonlocal last_masks
        key = (str(condition.action_type), str(condition.object_id))
        if key not in actions:
            raise RuntimeError("Unexpected active policy target")
        result = originals["_resolve_active_masks"](current, condition, *args, **kw)
        source = str(result[-1])
        if source not in {"sim_seg", "sim_missing"}:
            raise RuntimeError("Only current native target/rack body GT masks may condition the policy")
        last_masks = (np.asarray(result[1]).copy(), np.asarray(result[3]).copy(), condition.action_type_id, key, "active_action")
        mask_sources[source] += 1
        active_audit.append(dict(control_step=controls, action_type=key[0], object_id=key[1], mask_source=source,
            agent_area=0 if result[0] is None else int(np.count_nonzero(result[0])),
            wrist_area=0 if result[2] is None else int(np.count_nonzero(result[2]))))
        return result

    def previous_masks(current, episode, previous_object, action_type, *args, **kw):
        nonlocal last_masks
        if (str(action_type), str(previous_object)) != ("grasp", object_id):
            raise RuntimeError("Only the preceding target grasp may be rechecked")
        result = originals["_resolve_prev_completion_patches"](current, episode, previous_object, action_type, *args, **kw)
        last_masks = (np.asarray(result[0]).copy(), np.asarray(result[1]).copy(), conditions[0].action_type_id,
                      (str(action_type), str(previous_object)), "previous_completion")
        return result

    def infer(**payload):
        if last_masks is None:
            raise RuntimeError("Policy inference requires exact current mask resolution")
        third, wrist, action_type, key, kind = last_masks
        if (not np.array_equal(payload["masks"], third[None])
                or not np.array_equal(payload["wrist_masks"], wrist[None])
                or not np.array_equal(payload["text_feat"], text_feat[None])
                or payload["action_type"].tolist() != [action_type]):
            raise RuntimeError("Actual inference payload differs from current masks/text/action")
        inference_audit.append(dict(control_step=controls, action_type=key[0], object_id=key[1], inference_kind=kind,
            agent_mask_sha256=hashlib.sha256(payload["masks"].tobytes()).hexdigest(),
            wrist_mask_sha256=hashlib.sha256(payload["wrist_masks"].tobytes()).hexdigest(),
            text_feature_sha256=hashlib.sha256(payload["text_feat"].tobytes()).hexdigest()))
        return original_infer(**payload)

    _active_task = task_id
    env.reset, env.set_init_state, env.step, gpu_worker.infer = reset, set_state, step, infer
    exact.rollout.update_eval_tracker = update
    exact.rollout.custom_eval_now = lambda current, current_tracker: (bool(observer.complete), False)
    exact.rollout.custom_eval_success = lambda current_tracker: bool(observer.complete)
    exact.rollout.custom_eval_failed = lambda current_tracker: False
    exact.rollout._resolve_active_masks = active_masks
    exact.rollout._resolve_prev_completion_patches = previous_masks
    try:
        frames, success, meta = _base_episode(gpu_worker, env, init_state, text_feat, episode_data, conditions, **kwargs)
    finally:
        env.reset, env.set_init_state, env.step, gpu_worker.infer = original_reset, original_set, original_step, original_infer
        for name, function in originals.items():
            setattr(exact.rollout, name, function)
        _active_task = None
    if (len(initial_errors) != 1 or fixture_calls != 2 or settling_controls != 10
            or controls != meta["total_steps"] or bool(success) != observer.complete
            or len(observer.records) != controls+1):
        raise RuntimeError("Missing replay/control evidence or premature native predicate success")
    meta.update(rack_object_protocol=PROTOCOL, rack_object_task_id=task_id, rack_object_id=object_id,
        rack_object_placement=observer.as_dict(), rack_object_geometry=probe.geometry(),
        rack_object_mask_source_counts=dict(mask_sources), rack_object_active_mask_audit=active_audit,
        rack_object_inference_payload_audit=inference_audit,
        native_on_ever=any(r["native_on"] for r in observer.records), native_on_final=observer.records[-1]["native_on"],
        annotated_on_ever=any(r["annotated_on"] for r in observer.records), annotated_on_final=observer.records[-1]["annotated_on"],
        initial_state_sha256=snapshot["state_sha256"], init_state_index=snapshot["init_state_index"],
        fixture_replay_sha256=hashlib.sha256(replay_path.read_bytes()).hexdigest(), fixture_replay_calls=fixture_calls,
        initial_body_position_max_abs_diff=initial_errors[0], settling_control_steps=settling_controls,
        approved_layout_replay=True, final_tc_gate=False, native_predicate_required=False,
        legacy_native_on_auxiliary_only=True, annotated_predicate_required=True,
        both_action_conditioning_stages_observed={r["action_type"] for r in active_audit} == {"grasp", "release"},
        microwave_mask_scope="not_applicable", destination_mask_scope="original_whole_wine_rack_body",
        policy_action_generation_modified=False, policy_tc_switching_modified=False,
        success_reason="released_original_rack_top_deck_supported_placement" if success
                       else "strict_original_rack_placement_incomplete")
    return frames, success, meta


exact.evaluator.run_single_episode_libero_ex = rack_episode

if __name__ == "__main__":
    exact.evaluator.main()
