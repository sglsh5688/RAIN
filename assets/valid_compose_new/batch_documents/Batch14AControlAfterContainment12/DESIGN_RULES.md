# Batch 14A exact-donor placement/containment → control rules

- Each task uses one already evaluated atomic donor BDDL as its complete scene and copies exactly five donor states byte-for-byte. No fixture, object, region, or pose is synthesized or removed.
- Every instruction contains exactly two action-only clauses: placement/containment first, control second.
- Success is two strict ordered native events plus both final BDDL predicates. Compose final completion has no TC threshold.
- Retained drawer masks select only the requested moving drawer part, and retained stove control selects only `flat_stove_1_button`.
- The action added to the exact donor has a numeric source-pose proof in `SOURCE_COMPATIBILITY.json`.
- Every final predicate must be false after the evaluator-identical ten wait steps in all five states.
- Native articulation dead-bands are valid initial states: the builder never additionally requires `Close`, `Open`, `Turnoff`, or another opposite endpoint predicate.
- Every state must have empty initial and settled cross-entity penetration, every exact mask at least 10 pixels at 320×320, and deterministic replay within 1e-8 m.
- Every requested control passes a full current-to-native-endpoint articulation sweep with no cross-entity penetration and a true native endpoint predicate.
- Ordered sequence, unordered final-goal set, and semantic-alias final-goal set must be absent from LIBERO-40, selected Compose, every workspace `TASK_INDEX.tsv`, every workspace BDDL, every instrumented result, explicit VCN11–13 source definitions, and this batch's other candidates. Coverage of VCN1–13 is asserted.
- The immutable original 15-candidate physical-screen report is audited before build. Its 12 valid original IDs are mapped to contiguous retained IDs; all three physical exclusions and their measured collision reasons are preserved in selection manifests.
- Gripper trajectory is a soft empirical prior, not a hard exclusion rule.
