#!/usr/bin/env python3
"""Exactly five episodes, GPUs4/5, explicit future basket support contract only."""
import run_compose_traj_repair_basket_supported_entry as entry
import run_compose_traj_repair_5ep as launch
import yaml
from basket_released_support_observer import CONTRACT, BasketContactProbe

launch.ENTRYPOINT = launch.ROOT / "run_compose_traj_repair_basket_supported_entry.py"
_base_validate = launch.validate


def geometry_preflight(bundle, destinations):
    """Renderer-free CPU inspection of all five exact post-warmup states."""
    import json
    import numpy as np
    import torch
    from libero.libero.envs.env_wrapper import ControlEnv
    from cream_cheese_bowl_layout import apply_fixtures, state_hash
    states = torch.load(bundle / "task.pruned_init", map_location="cpu", weights_only=False)
    replay = json.loads((bundle / "FIXTURE_REPLAY.json").read_text())["rows"]
    env = ControlEnv(bddl_file_name=str(bundle / "task.bddl"), has_renderer=False,
                     has_offscreen_renderer=False, use_camera_obs=False, camera_names=[], ignore_done=True)
    records = []
    try:
        for index, state in enumerate(states):
            env.seed(7 + index)
            env.reset()
            poses = replay[index].get("fixture_model_poses", replay[index].get("fixture_snapshot"))
            apply_fixtures(env, poses)
            env.set_init_state(np.asarray(state))
            for _ in range(10):
                env.step([0, 0, 0, 0, 0, 0, -1])
            probe = BasketContactProbe(env, destinations)
            facts = probe.snapshot()
            if any(facts["entities"][name]["native_in"] for name in destinations):
                raise RuntimeError("Basket support preflight starts a native goal true")
            for name in set(destinations.values()):
                basket = facts["entities"][name]
                if (not basket["original_support_contact"] or not basket["upright"]
                        or basket["any_robot_contact"]
                        or basket["linear_speed_m_s"] > .02 or basket["angular_speed_rad_s"] > .5):
                    raise RuntimeError(f"Basket support preflight lacks stable supported basket: {index}/{name}")
            records.append(dict(state_index=index, initial_state_sha256=state_hash(state),
                                geometry=probe.geometry(), initial_snapshot=facts))
    finally:
        env.close()
    return records


def validate(args):
    tasks = _base_validate(args)
    for task in tasks:
        bundle = launch.Path(task["bundle"])
        meta = yaml.safe_load((bundle / "task_meta.yaml").read_text())
        rules = yaml.safe_load((bundle / "eval_rules.yaml").read_text())
        destinations = entry.validate_contract(meta, rules)
        task["basket_physical_contract"] = dict(CONTRACT)
        task["basket_target_destinations"] = destinations
        task["basket_support_geometry_preflight"] = geometry_preflight(bundle, destinations)
        task["basket_runtime_sources_sha256"] = {name: launch.digest(launch.ROOT / name) for name in (
            "basket_released_support_observer.py", "basket_supported_runtime.py",
            "run_compose_traj_repair_basket_supported_entry.py")}
    return tasks


launch.validate = validate
if __name__ == "__main__":
    launch.main()
