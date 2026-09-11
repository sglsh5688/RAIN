"""Explicit prospective terminal contract for mixed skills ending in basket placement."""
import re
from basket_released_support_observer import CONTRACT as PHYSICAL_CONTRACT

CONTRACT = dict(PHYSICAL_CONTRACT,
    basket_completion_mode='ordered_native_mixed_and_released_supported_settled_v1')
RUNTIME_FILES = (
    'basket_released_support_observer.py', 'basket_supported_runtime.py',
    'mixed_basket_contract.py', 'run_compose_traj_repair_mixed_basket_supported_entry.py',
    'run_compose_traj_repair_mixed_basket_supported_5ep.py',
)


def validate_contract(meta, rules):
    for source in [meta, rules]:
        for key, expected in CONTRACT.items():
            if source.get(key) != expected or isinstance(source.get(key), bool):
                raise RuntimeError(f'Explicit mixed basket contract required: {key}')
    atoms = rules.get('ordered_event_atoms') or []
    if (len(atoms) < 2 or len(set(atoms)) != len(atoms)
            or rules.get('required_goal_atoms') != atoms
            or meta.get('canonical_goal_atoms') != atoms
            or rules.get('continue_after_success') or rules.get('forbidden_goal_atoms')):
        raise RuntimeError('Mixed basket gate requires unchanged distinct ordered final goals')
    for key in ['custom_eval_needed', 'order_sensitive', 'requires_transition',
                'strict_event_order', 'final_success_requires_all_bddl_goals',
                'environment_ignore_done', 'downstream_preservation_required']:
        if rules.get(key) is not True:
            raise RuntimeError(f'Missing strict mixed native rule: {key}')
    if rules.get('final_tc_gate') is not False or rules.get('compose_final_tc_gate') is not False:
        raise RuntimeError('Mixed basket final TC must remain disabled')
    pairs, nonbasket = [], []
    for atom in atoms:
        match = re.fullmatch(r'in\(\s*([a-zA-Z0-9_]+)\s*,\s*(basket_[12])_contain_region\s*\)', atom)
        if match:
            pairs.append(match.groups())
        else:
            if not re.fullmatch(r'(?:on|in|open|close|turnon|turnoff)\([a-zA-Z0-9_, ]+\)', atom):
                raise RuntimeError('Unsupported mixed native predicate')
            nonbasket.append(atom)
    if (not pairs or not nonbasket or not atoms[-1].startswith('in(')
            or not re.fullmatch(r'in\(\s*([a-zA-Z0-9_]+)\s*,\s*(basket_[12])_contain_region\s*\)', atoms[-1])
            or len({p[0] for p in pairs}) != len(pairs)
            or any(p[0].startswith('basket_') for p in pairs)):
        raise RuntimeError('Require a mixed chain ending in distinct non-basket objects placed in baskets')
    return dict(pairs)
