# Batch37 basket + spatial-relation discovery

## Empirical source audit

- LBCM_005: cream-cheese-to-basket rose in 5/5; the full two-step task was 2/5.
- LBCM_001/002 and LBCM_007/008/017/018 already tested basket plus chocolate-pudding-right and are hard novelty exclusions.
- COMPOSE_346 nominally reached all predicates in 2/5, but success video review showed the last pudding path knocking over an earlier yellow mug; it is a negative downstream-preservation control, not a candidate donor sequence.
- New relations use evaluated ADAPT donors: butter-right 5/5, yellow-and-white-mug-right 4/5, BBQ-right 3/5, orange-juice-right 3/5.

## Candidate pool

| ID | Instruction |
|---|---|
| `VCN37_001` | Put the cream cheese box in the basket, then put the butter to the right of the plate. |
| `VCN37_002` | Put the butter to the right of the plate, then put the cream cheese box in the basket. |
| `VCN37_003` | Put the cream cheese box in the basket, then put the yellow and white mug to the right of the plate. |
| `VCN37_004` | Put the yellow and white mug to the right of the plate, then put the cream cheese box in the basket. |
| `VCN37_005` | Put the cream cheese box in the basket, then put the BBQ sauce to the right of the plate. |
| `VCN37_006` | Put the BBQ sauce to the right of the plate, then put the cream cheese box in the basket. |
| `VCN37_007` | Put the cream cheese box in the basket, then put the orange juice to the right of the plate. |
| `VCN37_008` | Put the orange juice to the right of the plate, then put the cream cheese box in the basket. |

## Hard gates

- All official LIBERO, selected Compose, prior evaluated, exact/unordered/semantic and instance-normalized ordered signatures are scanned before simulator use.
- State i is an exact robot-frame entity merge of LBCM_005 cream-cheese+basket and one evaluated ADAPT relation scene. No arbitrary XYZ, mirror or Z repair is permitted.
- No distractor is removed or moved in attempt 0. Any later removal requires measured collision/path-block evidence.
- All five states require initial goals false after ten no-op warm-up steps, no MuJoCo penetration, visible exact masks and deterministic replay.
- Runtime success requires strict ordered native rises and all final BDDL predicates, no final TC, and manual downstream-preservation review.

Static scan covered 1787 ordered prior signatures.
