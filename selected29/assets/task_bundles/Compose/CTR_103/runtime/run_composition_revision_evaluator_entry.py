#!/usr/bin/env python3
"""Approved scene replay + per-control-step ordered scoring, unchanged RAIN.

Only reset transforms and diagnostic/success observation are adapted. Action
generation, gripper actions, progress thresholds, and subtask switching are not
modified. Observing env.step also covers the shared rollout's forced-gripper
steps, which do not call its regular tracker callback.
"""
import hashlib
import json
from copy import deepcopy
from pathlib import Path

import run_diverse_adapt_evaluator_entry as exact
from composition_batch_order import OrderedEvents, parse_atom
from cream_cheese_bowl_layout import state_hash, apply_fixtures, position_error


def register_bindings():
    template = exact.benchmark_support.ACTION_OBJECTS['basket_1_contain_region']
    for basket in ('basket_1', 'basket_2'):
        for suffix in ('', '_contain_region'):
            source = deepcopy(template)
            for key in ('name', 'body_name'):
                if key in source:
                    source[key] = source[key].replace('basket_1', basket)
            exact.benchmark_support.ACTION_OBJECTS[basket + suffix] = source


register_bindings()
_episode = exact.evaluator.run_single_episode_libero_ex


def ordered_episode(gpu_worker, env, init_state, text_feat, episode_data, conditions, **kwargs):
    path = Path(kwargs['bddl_path']).parent / 'FIXTURE_REPLAY.json'
    payload = json.loads(path.read_text())
    candidates = [r for r in payload['rows'] if r['state_sha256'] == state_hash(init_state)]
    if len(candidates) != 1:
        raise RuntimeError('No unique fixture replay for this frozen initial state')
    snapshot = candidates[0]
    fixture_model_poses = snapshot.get('fixture_model_poses')
    if fixture_model_poses is None:
        # Newer physical screeners name the same authoritative root-pose map
        # ``fixture_snapshot``.  Accept the schema alias, but never silently
        # continue without a non-empty replay map.
        fixture_model_poses = snapshot.get('fixture_snapshot')
    # An explicitly stored empty map is valid for fixture-free tabletop
    # scenes; absence or a non-map value is not.
    if not isinstance(fixture_model_poses, dict):
        raise RuntimeError('Fixture replay has no authoritative fixture pose map')
    settled_body_positions = snapshot.get('settled_body_positions')
    atoms = list(kwargs['eval_rules']['ordered_event_atoms'])
    parsed = [parse_atom(a) for a in atoms]
    observer = OrderedEvents(atoms)
    originals = {name: getattr(exact.rollout, name) for name in
                 ('update_eval_tracker', 'custom_eval_now', 'custom_eval_success', 'custom_eval_failed')}
    reset_original, set_original, step_original = env.reset, env.set_init_state, env.step
    active_tracker = [None]
    counter = [0]
    initial_audit = []
    final_now = [False]
    replay_calls = [0]
    ordinary_callbacks = [0]

    def fixture_root_error(current):
        """Exact replay check for screeners that store fixture roots only."""
        errors = []
        for name, pose in fixture_model_poses.items():
            body_id = current.sim.model.body_name2id(name)
            actual_pos = current.sim.model.body_pos[body_id]
            actual_quat = current.sim.model.body_quat[body_id]
            errors.extend(abs(float(a) - float(b)) for a, b in zip(actual_pos, pose['model_body_pos']))
            errors.extend(abs(float(a) - float(b)) for a, b in zip(actual_quat, pose['model_body_quat']))
        return max(errors, default=0.0)

    def evaluate(current, tracker, step):
        originals['update_eval_tracker'](current, tracker, step)
        observer.update(step, [bool(current.env._eval_predicate(a)) for a in parsed])
        final_now[0] = bool(current.check_success())

    def reset(*args, **kw):
        obs = reset_original(*args, **kw)
        apply_fixtures(env, fixture_model_poses)
        replay_calls[0] += 1
        return obs

    def set_state(*args, **kw):
        apply_fixtures(env, fixture_model_poses)
        replay_calls[0] += 1
        return set_original(*args, **kw)

    def step(*args, **kw):
        result = step_original(*args, **kw)
        if active_tracker[0] is not None:
            counter[0] += 1
            evaluate(env, active_tracker[0], counter[0])
        return result

    def update(current, tracker, step_idx):
        step_idx = int(step_idx)
        if active_tracker[0] is None:
            if step_idx != 0:
                raise RuntimeError('Missing pre-policy step0 tracker initialization')
            error = (position_error(current, settled_body_positions)
                     if isinstance(settled_body_positions, dict)
                     else fixture_root_error(current))
            if error > 1e-8:
                raise RuntimeError(f'Approved frozen layout replay mismatch: {error}m')
            initial_audit.append(error)
            evaluate(current, tracker, 0)
            active_tracker[0] = tracker
        elif step_idx != counter[0]:
            raise RuntimeError(f'Control-step accounting differs: rollout={step_idx}, observed={counter[0]}')
        else:
            # env.step already updated the tracker exactly once for this step.
            ordinary_callbacks[0] += 1

    env.reset, env.set_init_state, env.step = reset, set_state, step
    exact.rollout.update_eval_tracker = update
    exact.rollout.custom_eval_now = lambda current, tracker: (observer.complete and bool(current.check_success()), bool(observer.violation))
    exact.rollout.custom_eval_success = lambda tracker: observer.complete and final_now[0]
    exact.rollout.custom_eval_failed = lambda tracker: bool(observer.violation)
    try:
        frames, success, meta = _episode(gpu_worker, env, init_state, text_feat, episode_data, conditions, **kwargs)
    finally:
        env.reset, env.set_init_state, env.step = reset_original, set_original, step_original
        for name, function in originals.items():
            setattr(exact.rollout, name, function)
    if len(initial_audit) != 1 or replay_calls[0] < 2:
        raise RuntimeError('Missing initial exact-layout replay audit')
    final_bddl = bool(env.check_success())
    success = bool(success and observer.complete and final_bddl)
    meta.update(composition_order=observer.as_dict(), final_bddl_success=final_bddl,
        approved_layout_replay=True,
        init_state_index=snapshot.get('init_state_index', snapshot.get('state_index')),
        initial_body_position_max_abs_diff=initial_audit[0],
        fixture_replay_schema=('settled_body_positions'
                               if isinstance(settled_body_positions, dict)
                               else 'fixture_snapshot_root_pose'),
        fixture_replay_calls=replay_calls[0], fixture_replay_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
        initial_state_sha256=snapshot['state_sha256'], all_control_steps_observed=counter[0],
        tracker_observation_scope='Every actual env.step after the standard wait, including forced gripper actions; no action/TC changes',
        success_reason='ordered_composition' if success else observer.violation or 'incomplete_composition')
    return frames, success, meta


exact.evaluator.run_single_episode_libero_ex = ordered_episode
if __name__ == '__main__':
    exact.evaluator.main()
