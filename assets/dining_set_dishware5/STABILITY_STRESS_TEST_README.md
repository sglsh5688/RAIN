# Dining-set destination diagnostics

`LOW_FRICTION_STABILITY_STRESS_TEST.json` is an exploratory stress test that asks an object to remain continuously `On` and in parent contact for 40 post-settling control samples. This is intentionally stricter than the benchmark's ordinary instantaneous LIBERO `On` success predicate.

The dining-set cloth collision has friction `0.001 0.001 0.001`; black bowl and ramekin poses can slide during this prolonged unattended test. Do not interpret its `all_passed: false` as task infeasibility. The authoritative policy evaluation produced at least one exact native-predicate success for every task (20/25 overall), with all success videos retained.

`earlier_transient_witnesses/` retains images from preliminary short-horizon contact probes only. They are not policy trials or success-rate evidence.
