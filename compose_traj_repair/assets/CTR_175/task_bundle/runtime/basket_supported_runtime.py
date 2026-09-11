"""Conjunct a future basket physical gate with the existing ordered callbacks."""
from basket_released_support_observer import BasketContactProbe, BasketSupportObserver


def run_supported_episode(rollout, inner_episode, worker, env, init_state, text_feat,
                          episode_data, conditions, destinations, *,
                          probe_factory=BasketContactProbe, **kwargs):
    names = ("update_eval_tracker", "custom_eval_now", "custom_eval_success", "custom_eval_failed")
    originals = {name: getattr(rollout, name) for name in names}
    original_step = env.step
    observer = BasketSupportObserver(destinations)
    tracker_ref, probe_ref = [None], [None]
    counter, ordinary_callbacks = [0], [0]

    def observe():
        observer.update(counter[0], probe_ref[0].snapshot())

    def step(*args, **kw):
        result = original_step(*args, **kw)
        if tracker_ref[0] is not None:
            counter[0] += 1
            observe()
        return result

    def update(current, tracker, step_idx):
        # Ordered's env.step has already observed every real control. Its
        # normal callback verifies the counter without advancing its observer.
        originals["update_eval_tracker"](current, tracker, step_idx)
        if tracker_ref[0] is None:
            if int(step_idx) != 0:
                raise RuntimeError("Missing basket post-warmup control zero")
            tracker_ref[0] = tracker
            probe_ref[0] = probe_factory(current, destinations)
            observe()
        elif int(step_idx) != counter[0]:
            raise RuntimeError(f"Basket control accounting differs: {step_idx} vs {counter[0]}")
        else:
            ordinary_callbacks[0] += 1

    def now(current, tracker):
        required, forbidden = originals["custom_eval_now"](current, tracker)
        return bool(required and observer.complete), forbidden

    def success(tracker):
        return bool(originals["custom_eval_success"](tracker) and observer.complete)

    env.step = step
    rollout.update_eval_tracker = update
    rollout.custom_eval_now = now
    rollout.custom_eval_success = success
    # custom_eval_failed is deliberately left identical to the ordered closure.
    try:
        frames, raw_success, meta = inner_episode(worker, env, init_state, text_feat,
                                                  episode_data, conditions, **kwargs)
        if tracker_ref[0] is None or counter[0] != int(meta["total_steps"]):
            raise RuntimeError("Basket observer missed actual policy controls")
        if counter[0] > int(kwargs["max_steps"]):
            raise RuntimeError("Basket run exceeded its unchanged policy cap")
        final = bool(success(tracker_ref[0]) and env.check_success())
        if bool(raw_success) != final:
            raise RuntimeError("Raw rollout bypassed ordered/native/physical basket conjunction")
        geometry = probe_ref[0].geometry()
    finally:
        env.step = original_step
        for name, function in originals.items():
            setattr(rollout, name, function)
    meta.update(basket_physical_completion=observer.as_dict(), basket_support_geometry=geometry,
                basket_completion_mode="ordered_native_and_released_supported_settled_v1",
                basket_native_order_and_final_required=True,
                basket_duplicate_callbacks_not_counted=ordinary_callbacks[0],
                basket_original_ordered_callbacks_conjoined=True,
                basket_final_native_bddl=bool(env.check_success()),
                basket_gate_raw_success=bool(raw_success),
                basket_policy_action_generation_modified=False,
                basket_policy_tc_switching_modified=False,
                basket_additional_controls_after_budget=0)
    return frames, final, meta
