# Batch 13 exact-donor high-priority Compose rules

- Each task uses one already evaluated donor BDDL as its entire physical scene and copies that donor's five serialized states byte-for-byte. No fixture, object, region, or pose is synthesized.
- Every task has exactly two action-only clauses, two strict ordered native events, and two final BDDL predicates.
- Final Compose termination is ordered native goals plus final BDDL only. There is no final TC threshold.
- Every action binds the exact manipulated object and target. Stove control masks only `flat_stove_1_button`; middle-drawer control masks only `wooden_cabinet_1:middle`.
- The additional action's object/fixture support region and every explicit target region must numerically match a learned or successfully evaluated source BDDL. These proofs are stored in `SOURCE_COMPATIBILITY.json`.
- All native goals must be false after the evaluator-identical ten wait steps. Exact donor states may remain in an articulation predicate dead-band; the endpoint sweep separately proves reachability.
- Every state must have empty initial/settled cross-entity penetration, every exact mask at least 10 pixels at 320x320, and a second frozen replay within 1e-8 m.
- A middle-drawer action must pass a complete initial-to-native-open sweep with no cross-entity penetration and a true native `Open` endpoint.
- Ordered sequence, unordered final-goal set, and semantic-alias final-goal set must be absent from all workspace TASK_INDEX files, BDDLs, instrumented result files, LIBERO-40, VCN Batch 11 source definitions, Batch 12's two retained source definitions, and this batch's other candidates.
- Gripper trajectory is a soft empirical prior, not a hard exclusion rule.
