# Batch 15 empirical exact-donor extension rules

- The pool is the 24 proposals in `BATCH14_EMPIRICAL_TRANSITION_AUDIT.md`. Twelve exact-scene control extensions entered the physical screen; eleven are retained. Twelve object-placement extensions are excluded because an exact original interacted pickup-slot proof is unavailable, and physical-screen candidate `VCN15_010` (audit rank 20) is excluded because opening the white middle drawer intersects `moka_pot_2` in all five donor states.
- Every retained task keeps a complete strict-success donor prefix and adds exactly one source-aligned drawer/stove control. One evaluated donor BDDL is the entire scene; no object, fixture, region, root, pose, or articulation state is edited.
- All five serialized donor states are copied byte-for-byte. Generated or resampled states are forbidden.
- Instructions contain only ordered action clauses. Wine manipulation is forbidden. Basket goals are absent (0/11, below the 25% cap).
- Every action masks its exact manipulated object and target. Drawer control selects only the requested moving part; stove control selects only `flat_stove_1_button`.
- All ordered final native predicates must be false after ten evaluator-identical wait steps. Native articulation dead-bands are allowed; no opposite-endpoint predicate is required.
- All five states must be initially and settled collision-free, all exact masks at least 10 pixels at 320x320, and all frozen replays within 1e-8 m.
- Every requested drawer/stove endpoint, including controls already in the retained prefix, must pass a full current-to-native-endpoint articulation sweep without cross-entity penetration.
- The full ordered sequence, unordered final-goal set, and semantic-alias final-goal set must be absent from every workspace `TASK_INDEX.tsv`, every workspace BDDL, all instrumented historical results, LIBERO-40, materialized/current VCN13, current Batch-14A/14B source definitions, and this batch.
- Success is strict ordered native events plus all final BDDL goals. Compose final termination has no TC threshold.
- Gripper trajectory is a soft empirical ranking prior, never a hard exclusion rule.
