#!/usr/bin/env python3
"""Strict Compose evaluation with observation-only full control traces.

Use only for the new trajectory-repair benchmark. Existing control, current
simulator masks, intermediate TC transitions and ordered native scoring are
delegated to the established evaluator without changing policy actions.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parent
RAIN_ROOT = ROOT.parent / "RAIN"
if str(RAIN_ROOT) not in sys.path:
    sys.path.insert(0, str(RAIN_ROOT))

import run_diverse_compose_evaluator_entry as ordered
from composition_batch_order import parse_atom
from cream_cheese_bowl_layout import fixture_snapshot, state_hash

exact = ordered.ordered.exact


def register_bindings():
    ordered.register_bindings()
    instances = (
        "akita_black_bowl_1", "akita_black_bowl_2", "alphabet_soup_1",
        "butter_1", "chocolate_pudding_1", "cream_cheese_1",
        "tomato_sauce_1", "milk_1", "salad_dressing_1", "orange_juice_1",
        "ketchup_1", "macaroni_and_cheese_1", "glazed_rim_porcelain_ramekin_1",
        "porcelain_mug_1", "porcelain_mug_2", "white_yellow_mug_1",
        "red_coffee_mug_1", "moka_pot_1", "moka_pot_2", "plate_1", "plate_2",
        "basket_1", "basket_2",
    )
    for name in instances:
        exact.benchmark_support.ACTION_OBJECTS[name] = dict(
            name=name + "_main", body_name=name + "_main",
            body_ids=[0], geom_ids=[], segmentable=True,
        )
    for name in ("basket_1", "basket_2"):
        exact.benchmark_support.ACTION_OBJECTS[name + "_contain_region"] = dict(
            exact.benchmark_support.ACTION_OBJECTS[name]
        )
    for object_id, body_name in {
        "flat_stove_1": "flat_stove_1_button",
        "flat_stove_1_cook_region": "flat_stove_1_burner",
        "wooden_cabinet_1_top_side": "wooden_cabinet_1_main",
        "wooden_cabinet_1_top_region": "wooden_cabinet_1_cabinet_top",
    }.items():
        exact.benchmark_support.ACTION_OBJECTS[object_id] = dict(
            name=body_name, body_name=body_name, body_ids=[0], geom_ids=[], segmentable=True,
        )


register_bindings()
_episode = exact.evaluator.run_single_episode_libero_ex
_prepare_text_cache = exact.evaluator._prepare_text_cache


def checked_text_cache(save_dir, bench, task_indices, clip_model_name, text_feature_dim):
    path = _prepare_text_cache(save_dir, bench, task_indices, clip_model_name, text_feature_dim)
    if clip_model_name != "openai/clip-vit-large-patch14" or int(text_feature_dim) != 768:
        raise RuntimeError("Trajectory-repair CLIP configuration differs from frozen RAIN")
    with np.load(path) as cache:
        for task_index in task_indices:
            description = bench.get_task(task_index).language
            feature = np.asarray(cache[description])
            if feature.shape != (768,) or not np.isfinite(feature).all() or np.linalg.norm(feature) < .99:
                raise RuntimeError("CLIP text feature is missing, zero, or nonfinite")
    return path


exact.evaluator._prepare_text_cache = checked_text_cache


def _rollout_context():
    """Read the existing rollout's counters without inserting a callback."""
    frame = sys._getframe(1)
    try:
        while frame is not None:
            if frame.f_code.co_name == "run_single_episode_libero_ex":
                values = frame.f_locals
                if "total_steps" not in values:
                    return -1, -1
                return int(values["total_steps"]), int(values.get("sub_idx", -1))
            frame = frame.f_back
        return -1, -1
    finally:
        del frame


def traced_episode(worker, env, init_state, text_feat, episode_data, conditions, **kwargs):
    rules = kwargs.get("eval_rules") or {}
    atoms = rules.get("ordered_event_atoms") or []
    if not (
        len(atoms) >= 2
        and rules.get("required_goal_atoms") == atoms
        and rules.get("strict_event_order") is True
        and rules.get("final_success_requires_all_bddl_goals") is True
        and rules.get("final_tc_gate") is False
        and rules.get("compose_final_tc_gate") is False
        and rules.get("environment_ignore_done") is True
        and rules.get("downstream_preservation_required") is True
        and int(kwargs.get("replan_steps", 8)) == 8
        and float(kwargs.get("feas_threshold", .7)) == .7
        and int(kwargs.get("consecutive_stop", 2)) == 2
        and int(kwargs.get("num_inference_steps", 4)) == 4
    ):
        raise RuntimeError("Trajectory-repair strict native/no-final-TC contract mismatch")
    gpu = int(os.environ.get("MUJOCO_EGL_DEVICE_ID", "-1"))
    if gpu not in (4, 5):
        raise RuntimeError(f"Trajectory-repair evaluation permits only physical GPUs 4/5: {gpu}")
    env.env.ignore_done = True
    bundle = Path(kwargs["bddl_path"]).parent
    import yaml
    metadata = yaml.safe_load((bundle / "task_meta.yaml").read_text())
    task_id = str(metadata["task_id"])
    initial_hash = state_hash(init_state)
    replay = json.loads((bundle / "FIXTURE_REPLAY.json").read_text())
    matches = [(i, row) for i, row in enumerate(replay["rows"]) if row["state_sha256"] == initial_hash]
    if len(matches) != 1:
        raise RuntimeError("Trace cannot resolve a unique frozen state index")
    state_index, replay_row = matches[0]
    trace_root = Path(os.environ["COMPOSE_TRAJ_TRACE_ROOT"])
    trace_root.mkdir(parents=True, exist_ok=True)
    stem = f"{task_id}_ep{state_index:03d}"
    parsed = [parse_atom(atom) for atom in atoms]
    model = env.sim.model
    body_names = [str(model.body_id2name(i)) for i in range(model.nbody)]
    site_names = [str(model.site_id2name(i)) for i in range(model.nsite)]
    grip_sites = [i for i, name in enumerate(site_names) if name.endswith("grip_site")]
    if not grip_sites:
        raise RuntimeError("Trace requires the native gripper grip_site")
    eef_site = grip_sites[0]
    gripper_joints = [name for name in model.joint_names if name.startswith("gripper")]
    snapshots, actions, control_steps, subtask_indices = [], [], [], []
    raw_contacts = []
    original_step = env.step

    def capture():
        data = env.sim.data
        return dict(
            sim_state=np.asarray(env.get_sim_state(), dtype=np.float64).copy(),
            body_pos=np.asarray(data.body_xpos, dtype=np.float64).copy(),
            body_quat=np.asarray(data.body_xquat, dtype=np.float64).copy(),
            eef_pos=np.asarray(data.site_xpos[eef_site], dtype=np.float64).copy(),
            eef_rotation=np.asarray(data.site_xmat[eef_site], dtype=np.float64).reshape(3, 3).copy(),
            gripper_qpos=np.asarray([float(data.get_joint_qpos(j)) for j in gripper_joints]),
            native_goals=np.asarray([bool(env.env._eval_predicate(atom)) for atom in parsed]),
            ctrl=np.asarray(data.ctrl, dtype=np.float64).copy(),
            qacc_warmstart=np.asarray(data.qacc_warmstart, dtype=np.float64).copy(),
        )

    def step(action, *args, **kw):
        control_step, subtask_index = _rollout_context()
        if not snapshots:
            snapshots.append(capture())
        action_copy = np.asarray(action, dtype=np.float64).copy()
        result = original_step(action, *args, **kw)
        actions.append(action_copy)
        control_steps.append(-1 if control_step < 0 else control_step + 1)
        subtask_indices.append(subtask_index)
        snapshots.append(capture())
        contacts = []
        for contact_index in range(env.sim.data.ncon):
            contact = env.sim.data.contact[contact_index]
            a = str(model.geom_id2name(int(contact.geom1)))
            b = str(model.geom_id2name(int(contact.geom2)))
            if "gripper" in a or "gripper" in b:
                contacts.append(dict(geom_a=a, geom_b=b, distance_m=float(contact.dist)))
        if contacts:
            raw_contacts.append(dict(raw_action_index=len(actions) - 1,
                                     control_step=control_steps[-1], contacts=contacts))
        return result

    env.step = step
    try:
        frames, nominal, meta = _episode(
            worker, env, init_state, text_feat, episode_data, conditions, **kwargs
        )
    finally:
        env.step = original_step
    native_final = [bool(env.env._eval_predicate(atom)) for atom in parsed]
    final_bddl = bool(env.check_success())
    success = bool(nominal and all(native_final) and final_bddl)
    if not snapshots or control_steps.count(-1) != 10:
        raise RuntimeError("Trace did not observe exactly ten native warm-up controls")
    policy_steps = [step for step in control_steps if step >= 0]
    if policy_steps != list(range(1, int(meta["total_steps"]) + 1)):
        raise RuntimeError("Trace control accounting does not match the established rollout")
    if int(meta["all_control_steps_observed"]) != len(policy_steps):
        raise RuntimeError("Trace and strict ordered observer disagree on control count")
    trace_path = trace_root / (stem + ".npz")
    temporary = trace_root / (stem + ".tmp.npz")
    arrays = {key: np.stack([snapshot[key] for snapshot in snapshots]) for key in snapshots[0]}
    np.savez_compressed(
        temporary, **arrays, actions=np.stack(actions),
        control_steps=np.asarray(control_steps, dtype=np.int32),
        subtask_indices=np.asarray(subtask_indices, dtype=np.int32),
        body_names=np.asarray(body_names), site_names=np.asarray(site_names),
        gripper_joint_names=np.asarray(gripper_joints),
    )
    temporary.replace(trace_path)
    audit = dict(
        protocol="compose_trajectory_repair_observation_only_v1",
        task_id=task_id, episode_index=state_index, initial_state_sha256=initial_hash,
        ordered_event_atoms=atoms, raw_action_count=len(actions), warmup_action_count=10,
        policy_control_count=len(policy_steps), success=success,
        body_position_frame="world", quaternion_convention="wxyz",
        eef_site=site_names[eef_site], fixture_model_poses=fixture_snapshot(env),
        frozen_fixture_replay=replay_row,
        trace_npz_sha256=hashlib.sha256(trace_path.read_bytes()).hexdigest(),
        gripper_contacts=raw_contacts, final_native_atom_values=native_final,
        all_final_bddl_predicates_true=final_bddl,
        policy_actions_modified=False, intermediate_tc_threshold=.7,
        intermediate_tc_consecutive=2, compose_final_tc_gate=False,
        replay_note=("NPZ snapshots[k] precede actions[k] and snapshots[k+1] follow them. "
                     "The first ten actions are the native warmup. Restore fixture model poses "
                     "before sim.set_state_from_flattened(snapshot); forward for state inspection. "
                     "Action replay also needs the original environment/controller reset; "
                     "snapshots alone do not serialize controller internals."),
        manual_semantic_video_review_required=True,
    )
    (trace_root / (stem + ".json")).write_text(json.dumps(audit, indent=2) + "\n")
    meta.update(
        trajectory_trace=dict(relative_path="traces/" + trace_path.name,
                              sha256=audit["trace_npz_sha256"],
                              raw_action_count=len(actions), policy_control_count=len(policy_steps),
                              observation_only=True),
        final_native_atom_values=native_final, final_bddl_success=final_bddl,
        final_tc_gate=False, compose_final_tc_gate=False,
        manual_success_video_preservation_review_required=True,
        publication_eligible=False,
    )
    if success:
        meta["success_reason"] = "ordered_native_goals_without_tc"
    return frames, success, meta


exact.evaluator.run_single_episode_libero_ex = traced_episode

if __name__ == "__main__":
    exact.evaluator.main()
