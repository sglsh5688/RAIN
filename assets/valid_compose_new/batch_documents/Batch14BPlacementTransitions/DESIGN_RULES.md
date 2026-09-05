# Batch 14B exact-donor placement-transition rules

- Every task has exactly two action-only clauses and uses one previously evaluated atomic donor BDDL as the complete scene.
- The donor BDDL and all five serialized donor states are retained byte-for-byte; no object, fixture, region, or articulation pose is synthesized.
- Basket goals are excluded. Wine bottles may remain unchanged distractors but are never manipulated.
- Ordered sequence, unordered final-goal set, and semantic-alias final-goal set must be absent from LIBERO-40, selected/historical workspace tasks and results, every VCN Batch 1--13 source definition, and this batch.
- Every action masks its exact manipulated object and target. Stove control masks only `flat_stove_1_button`; drawer control masks only the corresponding moving drawer part; microwave insertion targets only `microwave_1`; push targets only the exact stove-front region.
- All final goals must be false after the evaluator-identical ten wait steps. Every state must have no initial/settled cross-entity penetration, every exact mask must cover at least 10 pixels at 320x320, and frozen replay body error must be at most 1e-8 m.
- A middle-drawer-open action additionally requires a sweep from the actual settled initial joint value to the native `Open` endpoint without cross-entity penetration. The initial value may lie in the articulation dead-band; native `Close` is not required.
- Retained `VCN14B_010` (original physical-screen ID `VCN14B_013`) closes the same top drawer only after its first action removes the ramekin. Its dependent close sweep must therefore be interpreted at the post-prefix state during rollout review; no initial-state shortcut is accepted.
- Caddy suffixes retain the donor-native yellow-mug pose. Their caddy fixture/target geometry is exact, but the pickup transition is intentionally a medium-risk soft-trajectory probe.
- Gripper trajectory is a soft empirical prior, not a hard exclusion rule.
- Success is strict ordered native events plus final BDDL goals. Compose final termination has no TC threshold.
