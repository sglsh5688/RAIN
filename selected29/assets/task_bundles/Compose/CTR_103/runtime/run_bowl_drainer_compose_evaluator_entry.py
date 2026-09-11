#!/usr/bin/env python3
"""Two ordered, released-and-supported drainer placements; unchanged RAIN.

All changes are process-local scoring / audit / exact-mask adapters. Native In
predicates and the learned action / TC subtask-transition logic are unchanged.
In particular, native In for both objects must not terminate before release.
"""

from __future__ import annotations

from collections import Counter
from functools import lru_cache
from pathlib import Path

import numpy as np
import yaml

import run_diverse_adapt_evaluator_entry as strict
from novel_feedback_fixture_geometry import install_feedback_fixture_geometry
from novel_feedback_object_bindings import register_object_bindings
from novel_scene_mask_geometry import render_region_mask
from bowl_drainer_compose_geometry import (
    COMPARTMENT_TARGETS, FIXED_DRAINER_ROOT_XYZ, install_floor_drainer_support,
)
from bowl_drainer_ordered_placement_observer import (
    DrainerContactProbe, NATIVE_REGIONS, OrderedPlacementObserver,
)
from composition_batch_order import parse_atom


register_object_bindings()
install_feedback_fixture_geometry()
install_floor_drainer_support()
_episode = strict.exact_episode
_current_context = None


@lru_cache(maxsize=2048)
def task_spec(bddl_path):
    path = Path(bddl_path).resolve()
    meta = yaml.safe_load(path.with_name("task_meta.yaml").read_text())
    atoms = list(meta.get("canonical_goal_atoms") or [])
    hold = meta.get("support_hold_control_steps")
    if (meta.get("drainer_completion_mode") != "released_supported" or hold != 5
            or meta.get("semantic_subtask_count") != 2
            or meta.get("single_semantic_goal") is not False
            or meta.get("max_steps") != 1040):
        raise RuntimeError("Two placements require explicit released_supported, hold 5, budget 1040")
    OrderedPlacementObserver(atoms, hold)  # Validate distinct objects and one exact native site per stage.
    parsed = [parse_atom(atom) for atom in atoms]
    return dict(atoms=atoms, objects=[atom[1] for atom in parsed],
                regions=[atom[2] for atom in parsed], hold=hold, mode="released_supported")


def exact_region_mask(env, episode_data, object_id, bddl_path="",
                      image_size=256, camera_name="agentview"):
    binding = (episode_data or {}).get("objects", {}).get(str(object_id), {})
    if not binding or binding.get("segmentable", True):
        return None
    spec = task_spec(str(bddl_path))
    region = str(object_id)
    if region not in spec["regions"] or binding.get("name") != region:
        raise RuntimeError(f"Synthetic, union, or unknown destination requested: {object_id}")
    if _current_context is None or _current_context["active_index"] is None:
        raise RuntimeError("Region mask requested outside an audited action stage")
    active = _current_context["active_index"]
    expected = spec["regions"][active // 2]
    if region != expected:
        raise RuntimeError(f"Stage {active} requested {region}, expected exactly {expected}")
    mask = render_region_mask(env, Path(bddl_path), region, image_size, camera_name)
    audit = _current_context["mask_audit"]
    audit["requested_regions"][region] += 1
    audit["stage_region_calls"][f"{active}:{region}:{camera_name}"] += 1
    audit["calls"] += 1
    if mask is not None and np.any(mask):
        audit["nonempty_calls"] += 1
    return None if mask is None else np.ascontiguousarray(mask[:, ::-1])


def _physical_geometry(probe):
    sim, inner = probe.sim, probe.inner
    root = int(sim.model.body_name2id(inner.fixtures_dict["bowl_drainer_1"].root_body))
    position = np.asarray(sim.data.body_xpos[root])
    rotation = np.asarray(sim.data.body_xmat[root]).reshape(3, 3)
    if not np.allclose(position, FIXED_DRAINER_ROOT_XYZ, atol=1e-6, rtol=0):
        raise RuntimeError(f"Drainer root differs from the fixed two-compartment layout: {position}")
    if not np.allclose(rotation, np.eye(3), atol=1e-6, rtol=0):
        raise RuntimeError("Drainer orientation changed the robot-relative left/right meaning")
    sites = {}
    for side, record in COMPARTMENT_TARGETS.items():
        site_id = int(sim.model.site_name2id(record["native_region"]))
        actual = np.asarray(sim.data.site_xpos[site_id])
        if not np.allclose(actual, record["world_site_xyz"], atol=1e-6, rtol=0):
            raise RuntimeError(f"Native {side} compartment pose differs from its fixed definition")
        sites[side] = actual.tolist()
    return dict(passed=True, fixed_drainer_root_world_xyz=position.tolist(),
                native_site_world_xyz=sites, robot_left_world_axis="+Y",
                fixed_fixture_during_episode=True,
                native_base_geom_name=str(sim.model.geom_id2name(probe.base_geom)))


def ordered_placement_episode(gpu_worker, env, init_state, text_feat, episode_data, conditions, **kwargs):
    global _current_context
    spec = task_spec(str(kwargs["bddl_path"]))
    rules = dict(kwargs.get("eval_rules") or {})
    if (rules.get("required_goal_atoms") != spec["atoms"]
            or rules.get("ordered_event_atoms") != spec["atoms"]
            or rules.get("custom_eval_needed") is not True
            or rules.get("order_sensitive") is not True
            or str(rules.get("category", "")).lower() not in {"composition", "taskcomposition"}
            or rules.get("continue_after_success") or rules.get("forbidden_goal_atoms")
            or rules.get("sequence_stages")):
        raise RuntimeError("Runtime rules must explicitly require strict ordered final two-goal completion")
    if int(kwargs.get("max_steps", 0)) != 1040:
        raise RuntimeError("Two semantic placements must receive 1040 policy control steps")
    expected_actions = [
        ("grasp", spec["objects"][0]), ("release", spec["regions"][0]),
        ("grasp", spec["objects"][1]), ("release", spec["regions"][1]),
    ]
    actual_actions = [(str(condition.action_type), str(condition.object_id)) for condition in conditions]
    if actual_actions != expected_actions:
        raise RuntimeError(f"Wrong action/mask sequence: {actual_actions}; expected {expected_actions}")
    for object_id in spec["objects"]:
        binding = episode_data.get("objects", {}).get(object_id, {})
        if not binding.get("segmentable", True) or binding.get("body_name", binding.get("name")) not in {object_id, object_id + "_main"}:
            raise RuntimeError(f"Pickup binding is not the exact target instance: {object_id}")
    observer = OrderedPlacementObserver(spec["atoms"], spec["hold"])
    originals = {name: getattr(strict.rollout, name) for name in (
        "update_eval_tracker", "custom_eval_now", "custom_eval_success", "custom_eval_failed", "_resolve_active_masks",
    )}
    original_step = env.step
    tracker_ref, probe_ref = [None], [None]
    counter, ordinary_callbacks = [0], [0]
    snapshots = []
    initial_geometry = []
    context = dict(active_index=None,
                   mask_audit=dict(calls=0, nonempty_calls=0, requested_regions=Counter(), stage_region_calls=Counter()),
                   active_stage_audit=[])
    if _current_context is not None:
        raise RuntimeError("Nested ordered-placement episodes are not supported")
    _current_context = context

    def observe(current, tracker, step):
        originals["update_eval_tracker"](current, tracker, step)
        if probe_ref[0] is None:
            probe_ref[0] = DrainerContactProbe(current, spec["objects"])
            initial_geometry.append(_physical_geometry(probe_ref[0]))
        snapshot = probe_ref[0].snapshot()
        objects = snapshot["objects"]
        selected = [row["native_predicates"][region] for row, region in zip(objects, spec["regions"])]
        opposite = [row["native_predicates"][spec["regions"][1 - index]] for index, row in enumerate(objects)]
        observer.update(step, selected, opposite,
                        [row["native_base_contact"] for row in objects],
                        [row["any_gripper_contact"] for row in objects])
        if bool(current.check_success()) != bool(all(selected)):
            raise RuntimeError("Native simulator goal is not exactly the final two-compartment conjunction")
        if step == 0:
            snapshots.append(snapshot)

    def step(*args, **kw):
        result = original_step(*args, **kw)
        if tracker_ref[0] is not None:
            counter[0] += 1
            observe(env, tracker_ref[0], counter[0])
        return result

    def update(current, tracker, step_idx):
        if tracker_ref[0] is None:
            if int(step_idx) != 0:
                raise RuntimeError("Missing pre-policy control-step-zero initialization")
            observe(current, tracker, 0)
            tracker_ref[0] = tracker
        elif int(step_idx) != counter[0]:
            raise RuntimeError(f"Observed env.step count {counter[0]} differs from rollout {step_idx}")
        else:
            ordinary_callbacks[0] += 1  # Actual env.step already observed once.

    def active_masks(current, condition, *args, **kw):
        key = (str(condition.action_type), str(condition.object_id))
        if key not in expected_actions:
            raise RuntimeError(f"Unexpected inference condition: {key}")
        index = expected_actions.index(key)
        context["active_index"] = index
        result = originals["_resolve_active_masks"](current, condition, *args, **kw)
        mask_source = str(result[-1])
        expected_source = "sim_seg" if index % 2 == 0 else "sim_region"
        if mask_source != expected_source:
            raise RuntimeError(f"Stage {index} needs an exact live {expected_source} mask, got {mask_source}")
        context["active_stage_audit"].append(dict(control_step=counter[0], condition_index=index,
                                                  action_type=key[0], exact_mask_object_id=key[1],
                                                  destination_region=spec["regions"][index // 2], mask_source=mask_source))
        return result

    def now(current, tracker):
        return bool(observer.complete(spec["mode"]) and current.check_success()), bool(observer.violation(spec["mode"]))

    env.step = step
    strict.rollout.update_eval_tracker = update
    strict.rollout.custom_eval_now = now
    strict.rollout.custom_eval_success = lambda tracker: observer.complete(spec["mode"]) and bool(env.check_success())
    strict.rollout.custom_eval_failed = lambda tracker: bool(observer.violation(spec["mode"]))
    strict.rollout._resolve_active_masks = active_masks
    try:
        frames, raw_success, meta = _episode(gpu_worker, env, init_state, text_feat, episode_data, conditions, **kwargs)
        final_snapshot = probe_ref[0].snapshot()
        final_geometry = _physical_geometry(probe_ref[0])
    finally:
        env.step = original_step
        for name, function in originals.items():
            setattr(strict.rollout, name, function)
        _current_context = None
    if len(initial_geometry) != 1 or len(snapshots) != 1 or counter[0] != int(meta["total_steps"]):
        raise RuntimeError("Missing exact initial-state or per-control-step audit")
    success = bool(observer.complete(spec["mode"]) and env.check_success())
    if bool(raw_success) != success:
        raise RuntimeError("Rollout outcome bypassed the released/support ordered-final gate")
    if success and {row["condition_index"] for row in context["active_stage_audit"]} != {0, 1, 2, 3}:
        raise RuntimeError("Success lacks inference using all four exact stage masks")
    meta.update(
        drainer_completion_mode=spec["mode"], drainer_strict_support_rule="selected_native_In_AND_exact_bottom_box_contact_AND_no_gripper_contact_for_5_control_steps",
        drainer_ordered_placement=observer.as_dict(), drainer_initial_contacts=snapshots[0],
        drainer_final_contacts=final_snapshot, drainer_initial_geometry=initial_geometry[0],
        drainer_final_geometry=final_geometry, drainer_active_stage_masks=context["active_stage_audit"],
        drainer_exact_region_mask_audit={key: dict(value) if isinstance(value, Counter) else value
                                       for key, value in context["mask_audit"].items()},
        drainer_native_final_conjunction=bool(env.check_success()),
        drainer_raw_evaluator_success=bool(raw_success),
        drainer_native_success_is_auxiliary=True, drainer_observed_all_actual_control_steps=counter[0],
        drainer_duplicate_tracker_callbacks_not_double_counted=ordinary_callbacks[0],
        feedback_all_initial_goal_atoms_false=True,
        feedback_final_goals_satisfied=bool(env.check_success()),
        feedback_ordered_sequence_valid=bool(observer.released_supported.complete),
        feedback_semantic_subtask_count=2,
        policy_action_generation_modified=False, policy_tc_switching_modified=False,
        success_reason="ordered_released_supported_placements" if success else observer.violation(spec["mode"]) or "incomplete_ordered_released_supported_placements",
    )
    return frames, success, meta


strict.runtime.sim_region_mask_for_object_id = exact_region_mask
strict.rollout.sim_region_mask_for_object_id = exact_region_mask
strict.evaluator.run_single_episode_libero_ex = ordered_placement_episode


if __name__ == "__main__":
    strict.evaluator.main()
