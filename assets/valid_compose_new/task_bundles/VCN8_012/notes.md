# VCN8_012

- Instruction: Put the chocolate pudding on the black bowl, then close the middle drawer of the wooden cabinet.
- Family: `placement_then_control_soft_probe`
- Physical group: `anlgx_139__put_the_chocolate_pudding_on_the_black_bowl`
- Semantic components: `2`
- Pure original-atomic composition: `true`

## Components

1. Put the chocolate pudding on the black bowl — `on(chocolate_pudding_1, akita_black_bowl_1)`
2. Close the middle drawer of the wooden cabinet — `close(wooden_cabinet_1_middle_region)`

## Notes

- The placement atom retains the exact pudding_bowl donor object pose and five state variations.
- Only a drawer explicitly requested to close is opened at initialization; existing bottom-drawer openings are preserved.
- Trajectory continuity is a soft empirical prior, not an exclusion rule.
- Strict ordered native events and final BDDL determine success; Compose final completion has no TC threshold.
