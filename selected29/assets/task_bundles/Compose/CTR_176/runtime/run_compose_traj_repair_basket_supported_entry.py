#!/usr/bin/env python3
"""Future basket-only protocol: native order AND released supported settled5."""
from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent / "RAIN"))
import run_diverse_adapt_evaluator_entry as exact
from basket_released_support_observer import validate_contract
from basket_supported_runtime import run_supported_episode

_inner = exact.exact_episode


def future_basket_episode(worker, env, init_state, text_feat, episode_data, conditions, **kwargs):
    bundle = Path(kwargs["bddl_path"]).parent
    meta = yaml.safe_load((bundle / "task_meta.yaml").read_text())
    destinations = validate_contract(meta, kwargs.get("eval_rules") or {})
    if int(kwargs["max_steps"]) != int(meta["max_steps"]):
        raise RuntimeError("Future basket protocol must preserve the declared policy control cap")
    expected = [(action, target) for obj, basket in destinations.items()
                for action, target in (("grasp", obj), ("release", basket+"_contain_region"))]
    actual = [(str(c.action_type), str(c.object_id)) for c in conditions]
    if actual != expected:
        raise RuntimeError(f"Basket action/mask sequence differs from exact native goals: {actual}")
    return run_supported_episode(exact.rollout, _inner, worker, env, init_state, text_feat,
                                 episode_data, conditions, destinations, **kwargs)


# Ordered must capture this runner before installing its own callback layer.
exact.evaluator.run_single_episode_libero_ex = future_basket_episode
import run_compose_traj_repair_dual_stove_entry as trace
if trace.base.ordered.ordered._episode is not future_basket_episode:
    raise RuntimeError("Future basket gate imported too late to sit inside ordered evaluation")

if __name__ == "__main__":
    exact.evaluator.main()
