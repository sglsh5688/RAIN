#!/usr/bin/env python3
"""Mixed skills: all native goals/order AND basket release/support/settlement."""
from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent/'RAIN'))
import run_diverse_adapt_evaluator_entry as exact
from mixed_basket_contract import CONTRACT, validate_contract
from basket_supported_runtime import run_supported_episode

_inner = exact.exact_episode


def future_mixed_episode(worker, env, init_state, text_feat, episode_data, conditions, **kwargs):
    bundle = Path(kwargs['bddl_path']).parent
    meta = yaml.safe_load((bundle/'task_meta.yaml').read_text())
    destinations = validate_contract(meta, kwargs.get('eval_rules') or {})
    if int(kwargs['max_steps']) != int(meta['max_steps']):
        raise RuntimeError('Mixed support gate must retain its declared control cap')
    plan = yaml.safe_load((bundle/'action_plan.yaml').read_text())['steps']
    expected = [(p['action_type'], p['target_object_id'] if p['action_type']=='release'
                 else p['primary_object_id']) for p in plan]
    actual = [(str(c.action_type), str(c.object_id)) for c in conditions]
    if actual != expected:
        raise RuntimeError(f'Mixed action/mask sequence changed: {actual}')
    final_obj, final_basket = list(destinations.items())[-1]
    if actual[-2:] != [('grasp', final_obj), ('release', final_basket+'_contain_region')]:
        raise RuntimeError('Mixed terminal action must remain the requested final basket release')
    for cond, p in zip(conditions, plan):
        if (cond.source_task_description != p['source_task_description']
                or cond.source_subtask_index != p['source_subtask_index']):
            raise RuntimeError('Mixed source skill lineage differs from frozen action plan')
    frames, success, record = run_supported_episode(exact.rollout, _inner, worker, env,
        init_state, text_feat, episode_data, conditions, destinations, **kwargs)
    record.update(basket_completion_mode=CONTRACT['basket_completion_mode'],
        mixed_native_atoms_preserved=list(meta['canonical_goal_atoms']),
        mixed_nonbasket_goals_remain_required=True,
        mixed_physical_gate_scope='Only requested basket placements; every other native final goal remains conjoined and requires manual physical review.')
    return frames, success, record


exact.evaluator.run_single_episode_libero_ex = future_mixed_episode
import run_compose_traj_repair_dual_stove_entry as trace
if trace.base.ordered.ordered._episode is not future_mixed_episode:
    raise RuntimeError('Mixed support gate imported outside the ordered callback layer')

if __name__ == '__main__':
    exact.evaluator.main()
