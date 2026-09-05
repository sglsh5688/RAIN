# VCN8_007

- Instruction: Put the butter on the black bowl, then open the middle drawer of the cabinet.
- Family: `placement_then_open_transition`
- Physical group: `anlgx_138__put_the_butter_on_the_black_bowl`
- Semantic components: `2`
- Pure original-atomic composition: `true`

## Components

1. Put the butter on the black bowl — `on(butter_1, akita_black_bowl_1)`
2. Open the middle drawer of the cabinet — `open(wooden_cabinet_1_middle_region)`

## Notes

- The placement atom retains the exact butter_bowl donor object pose and five state variations.
- Only a drawer explicitly requested to close is opened at initialization; existing bottom-drawer openings are preserved.
- Trajectory continuity is a soft empirical prior, not an exclusion rule.
- Strict ordered native events and final BDDL determine success; Compose final completion has no TC threshold.
