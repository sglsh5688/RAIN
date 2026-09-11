#!/usr/bin/env python3
"""Diverse Adapt entrypoint: current simulator masks and initial-goal audit.

The shared evaluator is unchanged. These process-local adapters remove stored
mask inputs before inference and audit the simulator after its normal settling
steps. The original rollout, policy, success predicates and video writer run
unchanged.
"""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import numpy as np

from final_libero_ex_eval.impl import benchmark_support, evaluator, rollout, runtime
from run_analogy_evaluator_entry import EXTRA_ACTION_OBJECTS
from diverse_adapt_mask_geometry import render_region_mask


benchmark_support.ACTION_OBJECTS.update(EXTRA_ACTION_OBJECTS)
for object_id,body_name in {
    'basket_2':'basket_2_main',
    **{f'white_cabinet_2_{slot}_region':f'white_cabinet_2_cabinet_{slot}' for slot in ('top','middle','bottom')},
}.items():
    benchmark_support.ACTION_OBJECTS[object_id]=dict(name=body_name,body_name=body_name,body_ids=[0],geom_ids=[],segmentable=True)
_original_episode = evaluator.run_single_episode_libero_ex


def exact_region_mask(env, episode_data, object_id, bddl_path="", image_size=256, camera_name="agentview"):
    """Use current region geometry; match RAIN's 180-degree image convention."""
    obj=((episode_data or {}).get('objects',{}) or {}).get(str(object_id),{})
    if not obj or bool(obj.get('segmentable',True)): return None
    name=str(obj.get('name',''))
    if 'region' not in name: return None
    mask=render_region_mask(env,Path(bddl_path),name,image_size,camera_name)
    return None if mask is None else np.ascontiguousarray(mask[:,::-1])


runtime.sim_region_mask_for_object_id=exact_region_mask
rollout.sim_region_mask_for_object_id=exact_region_mask


def exact_episode(gpu_worker, env, init_state, text_feat, episode_data, conditions, **kwargs):
    patch_count = (int(kwargs.get("dino_input_size", 224)) // 14) ** 2
    conditions = [
        replace(
            condition,
            mask_raw=None,
            mask_patches=np.zeros(patch_count, dtype=np.float32),
            wrist_mask_raw=None,
            wrist_mask_patches=np.zeros(patch_count, dtype=np.float32),
        )
        for condition in conditions
    ]
    # Placement and transition helpers may otherwise consult training JSON.
    kwargs["source_episodes"] = None
    original_tracker_update = rollout.update_eval_tracker
    initial_checks = []

    def checked_tracker_update(current_env, tracker, step_idx):
        original_tracker_update(current_env, tracker, step_idx)
        if int(step_idx) == 0:
            initial_goal = bool(current_env.check_success())
            initial_checks.append(initial_goal)
            if initial_goal:
                raise RuntimeError("Diverse Adapt goal is already true before policy inference")

    # The microwave interaction binding must resolve only its articulated door.
    for condition in conditions:
        if condition.object_id == "microwave_1":
            obj = episode_data["objects"]["microwave_1"]
            if obj.get("body_name", obj.get("name")) != "microwave_1_microdoorroot":
                raise RuntimeError("microwave interaction does not bind the door body")
            expected = int(env.sim.model.body_name2id("microwave_1_microdoorroot"))
            actual = list((kwargs.get("corrected_bids") or {}).get("microwave_1", []))
            if actual != [expected]:
                raise RuntimeError(f"microwave door body mismatch: {actual}, expected {[expected]}")

    rollout.update_eval_tracker = checked_tracker_update
    try:
        frames, success, meta = _original_episode(
            gpu_worker, env, init_state, text_feat, episode_data, conditions, **kwargs
        )
    finally:
        rollout.update_eval_tracker = original_tracker_update
    if initial_checks != [False]:
        raise RuntimeError(f"missing or repeated initial-goal audit: {initial_checks}")
    meta.update(
        initial_goal_satisfied=False,
        initial_goal_check="current_simulator_after_standard_settling_before_inference",
        stored_mask_fallback_enabled=False,
        microwave_mask_scope="door_only",
        stove_turn_mask_scope="knob_only",
    )
    return frames, success, meta


# Multiprocessing spawn imports this entrypoint before invoking evaluator.worker.
evaluator.run_single_episode_libero_ex = exact_episode


if __name__ == "__main__":
    evaluator.main()
