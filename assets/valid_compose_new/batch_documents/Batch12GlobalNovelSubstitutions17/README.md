# Batch 12: Global-Novel Exact-Slot Substitutions

The original pool had 17 globally novel semantics. Two pass the exact single-scene/frozen-state/pickup-slot, visibility, and learned-orientation rules; 15 are documented in `EXCLUDED_CANDIDATES.tsv`.

| ID | Original proposal | Instruction | Replacement Object donor |
|---|---|---|---|
| `VCN12_001` | `C1` | Put the tomato sauce in the basket, then put the white mug on the left plate, and finally put the cream cheese box in the basket. | `LIBERO_OBJECT_06` |
| `VCN12_002` | `C2` | Put the salad dressing in the basket, then put the white mug on the left plate, and finally put the cream cheese box in the basket. | `LIBERO_OBJECT_03` |

## Validation


- The audited proposal pool contains 17 globally novel goal sets. Two satisfy the exact physical donor, five-state visibility, and learned-orientation gates; fifteen are explicitly excluded rather than synthesized by arbitrary layout mixing.
- Every retained task is a controlled one-object substitution of evaluated LBCM_028. Fixture roots, region definitions, unrelated objects and the five serialized donor states remain byte-identical.
- The replacement object's original LIBERO-Object target pickup rectangle and yaw must numerically equal LBCM_028's retained alphabet-soup slot.
- Every semantic action binds the exact manipulated object and its exact target. All rendered masks must contain at least 10 pixels at 320x320 in every state.
- All three native goals must be false after the evaluator-identical ten wait steps. Initial and settled cross-entity penetration must be empty.
- Every second frozen replay must match all body positions within 1e-8 m. Because a changed object mesh can settle slightly from the byte-identical initial generalized coordinate, its post-wait root must remain within 2 mm of the exact pickup rectangle on both deterministic passes; no pose is edited to obtain this tolerance.
- Success requires strict ordered native events and all final BDDL predicates. Compose final termination has no TC threshold.
- Ordered sequence, unordered final-goal set, and semantic-alias final-goal set must be absent from all workspace TASK_INDEX files, task BDDLs, instrumented past results, LIBERO-40, Batch 11 source definitions, and this batch's other proposals.
- Gripper trajectory is a soft empirical prior, not an exclusion rule.

