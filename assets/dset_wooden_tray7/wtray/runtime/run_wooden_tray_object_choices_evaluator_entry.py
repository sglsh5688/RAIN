#!/usr/bin/env python3
"""Exact-mask, strictly physical evaluator for atomic wooden-tray tasks.

The RAIN policy, action plans, transition controller, native sites, and assets
are unchanged.  Success is an evaluation-only conjunction held for five actual
control steps: native ``In``, full collision-envelope containment, positive-
force tray contact, and no gripper contact.
"""

from __future__ import annotations

from collections import Counter
from functools import lru_cache
from pathlib import Path
import re

import numpy as np
import yaml

import run_diverse_adapt_evaluator_entry as strict
from novel_scene_mask_geometry import render_region_mask
from wooden_tray_object_choices_support import (
    SUPPORTED_MANIPULANDS,
    TARGET_REGION,
    install_wooden_tray_object_choices_support,
    register_object_bindings,
)
from wooden_tray_strict_placement_observer import (
    StrictTrayPlacementObserver,
    WoodenTrayContactProbe,
)


register_object_bindings()
install_wooden_tray_object_choices_support()
_episode = strict.exact_episode
_current_context = None


def parse_single_tray_atom(atom: str) -> str:
    match = re.fullmatch(
        r"\s*in\s*\(\s*([^,()\s]+)\s*,\s*([^,()\s]+)\s*\)\s*",
        str(atom),
        flags=re.IGNORECASE,
    )
    if match is None or match.group(2).casefold() != TARGET_REGION.casefold():
        raise ValueError(f"Expected one In(object, {TARGET_REGION}) atom: {atom}")
    object_id = match.group(1)
    if object_id not in SUPPORTED_MANIPULANDS:
        raise ValueError(f"Unsupported wooden-tray manipuland: {object_id}")
    return object_id


@lru_cache(maxsize=2048)
def task_spec(bddl_path: str) -> dict:
    path = Path(bddl_path).resolve()
    meta = yaml.safe_load(path.with_name("task_meta.yaml").read_text())
    atoms = list(meta.get("canonical_goal_atoms") or [])
    if len(atoms) != 1:
        raise RuntimeError("Wooden-tray choice tasks require exactly one goal atom")
    object_id = parse_single_tray_atom(atoms[0])
    hold = meta.get("support_hold_control_steps")
    if (
        meta.get("tray_completion_mode")
        != "full_containment_released_supported"
        or hold != 5
        or meta.get("semantic_subtask_count") != 1
        or meta.get("single_semantic_goal") is not True
        or meta.get("max_steps") != 520
        or meta.get("full_collision_containment_required") is not True
        or meta.get("positive_force_tray_contact_required") is not True
        or meta.get("no_gripper_contact_required") is not True
        or meta.get("target_support_site") != TARGET_REGION
    ):
        raise RuntimeError(
            "Atomic tray tasks require the explicit strict physical hold-5 protocol"
        )
    return {
        "atoms": atoms,
        "object_id": object_id,
        "region": TARGET_REGION,
        "hold": hold,
    }


def exact_region_mask(
    env,
    episode_data,
    object_id,
    bddl_path="",
    image_size=256,
    camera_name="agentview",
):
    """Project only the current native tray site, never a stored/union mask."""
    binding = (episode_data or {}).get("objects", {}).get(str(object_id), {})
    if not binding or binding.get("segmentable", True):
        return None
    spec = task_spec(str(bddl_path))
    region = str(object_id)
    if region != spec["region"] or binding.get("name") != region:
        raise RuntimeError(f"Synthetic, union, or unknown tray region: {region}")
    if _current_context is None:
        raise RuntimeError("Tray region mask requested outside an active episode")
    active_index = _current_context["active_index"]
    # The rollout asks for the *next* release-region mask while it is still
    # executing the grasp stage, then asks for it again during release.  Both
    # calls must project the same current native tray site; neither is a stored
    # or union mask.
    if active_index not in {0, 1}:
        raise RuntimeError("Tray region mask requested outside an active stage")
    mask = render_region_mask(
        env, Path(bddl_path), region, image_size, camera_name
    )
    audit = _current_context["mask_audit"]
    audit["calls"] += 1
    audit["requested_regions"][region] += 1
    audit["stage_region_calls"][f"{active_index}:{region}:{camera_name}"] += 1
    if mask is not None and np.any(mask):
        audit["nonempty_calls"] += 1
    return None if mask is None else np.ascontiguousarray(mask[:, ::-1])


def strict_tray_episode(
    gpu_worker,
    env,
    init_state,
    text_feat,
    episode_data,
    conditions,
    **kwargs,
):
    global _current_context
    spec = task_spec(str(kwargs["bddl_path"]))
    rules = dict(kwargs.get("eval_rules") or {})
    if (
        rules.get("required_goal_atoms") != spec["atoms"]
        or rules.get("custom_eval_needed") is not True
        or rules.get("order_sensitive") is not False
        or rules.get("requires_transition") is not False
        or rules.get("continue_after_success") is not False
        or rules.get("forbidden_goal_atoms")
        or rules.get("sequence_stages")
    ):
        raise RuntimeError("Runtime rules must require one strict atomic tray goal")
    if int(kwargs.get("max_steps", 0)) != 520:
        raise RuntimeError("Atomic wooden-tray tasks require 520 policy control steps")

    expected_actions = [
        ("grasp", spec["object_id"]),
        ("release", spec["region"]),
    ]
    actual_actions = [
        (str(condition.action_type), str(condition.object_id))
        for condition in conditions
    ]
    if actual_actions != expected_actions:
        raise RuntimeError(
            f"Wrong action/mask sequence: {actual_actions}; expected {expected_actions}"
        )
    pickup_binding = episode_data.get("objects", {}).get(spec["object_id"], {})
    if (
        not pickup_binding.get("segmentable", True)
        or pickup_binding.get("body_name", pickup_binding.get("name"))
        != spec["object_id"] + "_main"
    ):
        raise RuntimeError("Pickup binding is not the exact selected instance")
    region_binding = episode_data.get("objects", {}).get(spec["region"], {})
    if (
        region_binding.get("segmentable", True)
        or region_binding.get("name") != spec["region"]
    ):
        raise RuntimeError("Release binding is not the exact native tray site")

    observer = StrictTrayPlacementObserver(spec["hold"])
    originals = {
        name: getattr(strict.rollout, name)
        for name in (
            "update_eval_tracker",
            "custom_eval_now",
            "custom_eval_success",
            "custom_eval_failed",
            "_resolve_active_masks",
        )
    }
    original_step = env.step
    tracker_ref = [None]
    probe_ref = [None]
    counter = [0]
    duplicate_tracker_callbacks = [0]
    initial_snapshots: list[dict] = []
    context = {
        "active_index": None,
        "mask_audit": {
            "calls": 0,
            "nonempty_calls": 0,
            "requested_regions": Counter(),
            "stage_region_calls": Counter(),
        },
        "active_stage_audit": [],
    }
    if _current_context is not None:
        raise RuntimeError("Nested strict wooden-tray episodes are unsupported")
    _current_context = context

    def observe(current, tracker, step: int) -> None:
        originals["update_eval_tracker"](current, tracker, step)
        if probe_ref[0] is None:
            probe_ref[0] = WoodenTrayContactProbe(current, spec["object_id"])
        snapshot = probe_ref[0].snapshot()
        observer.update(step, snapshot)
        native_goal = bool(current.check_success())
        if native_goal != bool(snapshot["native_in"]):
            raise RuntimeError("BDDL success differs from the single native tray In goal")
        if step == 0:
            initial_snapshots.append(snapshot)

    def step(*args, **step_kwargs):
        result = original_step(*args, **step_kwargs)
        if tracker_ref[0] is not None:
            counter[0] += 1
            observe(env, tracker_ref[0], counter[0])
        return result

    def update(current, tracker, step_idx):
        if tracker_ref[0] is None:
            if int(step_idx) != 0:
                raise RuntimeError("Missing pre-policy control-step-zero observation")
            observe(current, tracker, 0)
            tracker_ref[0] = tracker
        elif int(step_idx) != counter[0]:
            raise RuntimeError(
                f"Observed env.step count {counter[0]} differs from rollout {step_idx}"
            )
        else:
            duplicate_tracker_callbacks[0] += 1

    def active_masks(current, condition, *args, **mask_kwargs):
        key = (str(condition.action_type), str(condition.object_id))
        if key not in expected_actions:
            raise RuntimeError(f"Unexpected inference condition: {key}")
        index = expected_actions.index(key)
        context["active_index"] = index
        result = originals["_resolve_active_masks"](
            current, condition, *args, **mask_kwargs
        )
        source = str(result[-1])
        # A manipulated object can leave both cameras after a failed motion.
        # That is an ordinary failed rollout state, not a harness failure.  In
        # that case the strict no-fallback adapter deliberately supplies a
        # zero current-simulator mask and labels it ``sim_missing`` (or
        # ``sim_region_missing`` for the native site).  Never replace it with
        # a stored JSON mask, but let the episode run to a scored outcome.
        expected_sources = (
            {"sim_seg", "sim_missing"}
            if index == 0
            else {"sim_region", "sim_region_missing"}
        )
        if source not in expected_sources:
            raise RuntimeError(
                f"Stage {index} needs a current-simulator mask or an explicit "
                f"current-simulator missing mask, got {source}"
            )
        context["active_stage_audit"].append(
            {
                "control_step": counter[0],
                "condition_index": index,
                "action_type": key[0],
                "exact_mask_object_id": key[1],
                "mask_source": source,
            }
        )
        return result

    def now(current, tracker):
        return bool(observer.complete and current.check_success()), False

    env.step = step
    strict.rollout.update_eval_tracker = update
    strict.rollout.custom_eval_now = now
    strict.rollout.custom_eval_success = lambda tracker: bool(
        observer.complete and env.check_success()
    )
    strict.rollout.custom_eval_failed = lambda tracker: False
    strict.rollout._resolve_active_masks = active_masks
    try:
        frames, raw_success, meta = _episode(
            gpu_worker,
            env,
            init_state,
            text_feat,
            episode_data,
            conditions,
            **kwargs,
        )
        final_snapshot = probe_ref[0].snapshot()
    finally:
        env.step = original_step
        for name, function in originals.items():
            setattr(strict.rollout, name, function)
        _current_context = None

    if (
        len(initial_snapshots) != 1
        or counter[0] != int(meta["total_steps"])
        or observer.last_step != counter[0]
    ):
        raise RuntimeError("Missing exact initial-state or per-control-step audit")
    success = bool(observer.complete and env.check_success())
    if bool(raw_success) != success:
        raise RuntimeError("Rollout outcome bypassed strict wooden-tray scoring")
    if success and {
        int(row["condition_index"]) for row in context["active_stage_audit"]
    } != {0, 1}:
        raise RuntimeError("Success lacks both exact pickup and release mask stages")

    mask_audit = {
        key: dict(value) if isinstance(value, Counter) else value
        for key, value in context["mask_audit"].items()
    }
    strict_reason = (
        "full_containment_released_supported_hold5"
        if success
        else "incomplete_strict_wooden_tray_placement"
    )
    meta.update(
        tray_completion_mode="full_containment_released_supported",
        tray_strict_support_rule=(
            "native_In_AND_full_collision_envelope_inside_native_site_1mm_"
            "AND_positive_force_tray_contact_AND_no_gripper_contact_hold5"
        ),
        tray_strict_placement=observer.as_dict(),
        tray_initial_physical_snapshot=initial_snapshots[0],
        tray_final_physical_snapshot=final_snapshot,
        tray_active_stage_masks=context["active_stage_audit"],
        tray_exact_region_mask_audit=mask_audit,
        tray_native_final_goal=bool(env.check_success()),
        tray_raw_evaluator_success=bool(raw_success),
        tray_native_success_is_auxiliary=True,
        tray_observed_all_actual_control_steps=counter[0],
        tray_duplicate_tracker_callbacks_not_double_counted=(
            duplicate_tracker_callbacks[0]
        ),
        feedback_all_initial_goal_atoms_false=True,
        feedback_final_goals_satisfied=bool(env.check_success()),
        feedback_ordered_sequence_valid=True,
        feedback_semantic_subtask_count=1,
        policy_action_generation_modified=False,
        policy_tc_switching_modified=False,
        success_reason=strict_reason,
        termination_reason=strict_reason,
    )
    return frames, success, meta


strict.runtime.sim_region_mask_for_object_id = exact_region_mask
strict.rollout.sim_region_mask_for_object_id = exact_region_mask
strict.evaluator.run_single_episode_libero_ex = strict_tray_episode


if __name__ == "__main__":
    strict.evaluator.main()
