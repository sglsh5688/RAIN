#!/usr/bin/env python3
"""Exact-mask evaluator for dishware placement on a dining-set mat."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from dining_set_dishware_support import (
    install_dining_set_dishware_support,
    register_object_bindings,
)
import run_diverse_adapt_evaluator_entry as strict
from novel_feedback_eval_support import final_sequence_valid, install_feedback_eval_support


register_object_bindings()
install_dining_set_dishware_support()
install_feedback_eval_support()


def exact_region_mask(
    env,
    episode_data,
    object_id,
    bddl_path="",
    image_size=256,
    camera_name="agentview",
):
    binding = (episode_data or {}).get("objects", {}).get(str(object_id), {})
    if not binding or binding.get("segmentable", True):
        return None
    from novel_scene_mask_geometry import render_region_mask

    mask = render_region_mask(
        env, Path(bddl_path), binding["name"], image_size, camera_name
    )
    return None if mask is None else np.ascontiguousarray(mask[:, ::-1])


def dining_set_episode(*args, **kwargs):
    frames, success, meta = strict.exact_episode(*args, **kwargs)
    env = args[1] if len(args) > 1 else kwargs["env"]
    rules = dict(kwargs.get("eval_rules") or {})
    final_goals = bool(env.check_success())
    sequence_valid = final_sequence_valid(meta, rules, final_goals)
    success = bool(success and final_goals and sequence_valid)
    meta.update(
        feedback_all_initial_goal_atoms_false=True,
        feedback_final_goals_satisfied=final_goals,
        feedback_ordered_sequence_valid=sequence_valid,
        feedback_semantic_subtask_count=1,
        dining_set_support_site="physical_exposed_mat_between_utensils",
        dining_set_parent_contact_required=True,
    )
    return frames, success, meta


strict.runtime.sim_region_mask_for_object_id = exact_region_mask
strict.rollout.sim_region_mask_for_object_id = exact_region_mask
strict.evaluator.run_single_episode_libero_ex = dining_set_episode


if __name__ == "__main__":
    strict.evaluator.main()
