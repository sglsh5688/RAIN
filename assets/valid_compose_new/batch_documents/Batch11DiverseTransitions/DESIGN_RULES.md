# Batch 11 diverse-transition Compose rules

- Fifteen candidates use one evaluated donor BDDL and its five frozen states byte-for-byte. No fixture, object, or articulation pose is changed.
- Every task has exactly two strict ordered native events and two final BDDL predicates.
- Final Compose termination is ordered native goals plus final BDDL only; there is no final TC threshold.
- Each semantic manipulation binds its exact object and target. Stove control masks only `flat_stove_1_button`; wooden-drawer control masks only `wooden_cabinet_1:top`.
- Initial native goals must all be false after the evaluator's ten wait steps. Drawer-close tasks retain the exact partially-open atomic donor state and must pass a full native close sweep; they need not satisfy the stricter native `Open` threshold.
- Every state must have no initial/settled cross-entity penetration, all mask areas at least 10 pixels at 320x320, an exact second replay within 1e-8 m, and a unique frozen-state hash.
- Drawer-close candidates must pass a full initial-to-native-close sweep with no cross-entity penetration and a true native `Close` endpoint.
- Ordered sequences and unordered final-goal sets are rejected if they overlap LIBERO-40, selected Compose, or VCN Batch 1-10. Internal ordered and final-set duplicates are also rejected.
- Gripper trajectory continuity is recorded as a soft empirical prior, not a hard exclusion rule.
