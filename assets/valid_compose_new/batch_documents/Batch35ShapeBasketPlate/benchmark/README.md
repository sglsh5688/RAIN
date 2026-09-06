# Batch35 · shape-cross-target basket + plate Compose

The 16 requested concrete combinations (2 round identities × 2 cylindrical identities × 2 plate instances × 2 orders) are recorded in `CANDIDATE_CENSUS.tsv`. The discovery screen retains all four right-plate round-first identity pairs plus one reverse-order representative (five tasks, four physical scenes). Identity-normalized redundancy is metadata for final diversity selection, not an empirical pre-filter.

## Retained candidates

| ID | Instruction | Exact source union |
|---|---|---|
| VCN35_001 | Put the black bowl in the basket, then put the alphabet soup on the right plate. | SOUP_RIGHT + BLACK_BOWL + BASKET |
| VCN35_002 | Put the tomato sauce on the right plate, then put the ramekin in the basket. | TOMATO_RIGHT + RAMEKIN + BASKET |
| VCN35_003 | Put the black bowl in the basket, then put the tomato sauce on the right plate. | TOMATO_RIGHT + BLACK_BOWL + BASKET |
| VCN35_004 | Put the ramekin in the basket, then put the alphabet soup on the right plate. | SOUP_RIGHT + RAMEKIN + BASKET |
| VCN35_005 | Put the ramekin in the basket, then put the tomato sauce on the right plate. | TOMATO_RIGHT + RAMEKIN + BASKET |

## Hard gates

- Official/selected/all-prior exact ordered, concrete unordered, semantic and identity-normalized ordered duplicates are rejected before simulator use.
- State i uses only exact state-i donor entity transforms in the robot frame. No random XYZ, mirror, offset, or support-only Z repair is permitted.
- The non-target plate always remains. The red mug remains in black-bowl scenes; it is removed only in ramekin scenes after attempt1 state 0 showed direct 0.883–5.203 mm red-mug/ramekin MuJoCo penetration. No required object is moved.
- Every goal must be false after the evaluator's ten no-op warm-up steps; all five states need no MuJoCo penetration, stable donor fidelity, visible exact masks, and deterministic replay.
- Runtime success requires strict ordered native rises plus all final BDDL goals, with no final TC gate. Downstream preservation requires later actions not to damage the earlier relation.

Static scan covered 1779 ordered prior signatures.
