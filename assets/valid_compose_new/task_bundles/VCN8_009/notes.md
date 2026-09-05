# VCN8_009

- Instruction: Put the cream cheese on the stove, then open the middle drawer of the cabinet.
- Family: `placement_then_open_transition`
- Physical group: `anlgx_127__put_the_cream_cheese_on_the_stove`
- Semantic components: `2`
- Pure original-atomic composition: `true`

## Components

1. Put the cream cheese on the stove — `on(cream_cheese_1, flat_stove_1_cook_region)`
2. Open the middle drawer of the cabinet — `open(wooden_cabinet_1_middle_region)`

## Notes

- The placement atom retains the exact cheese_stove donor object pose and five state variations.
- Only a drawer explicitly requested to close is opened at initialization; existing bottom-drawer openings are preserved.
- Trajectory continuity is a soft empirical prior, not an exclusion rule.
- Strict ordered native events and final BDDL determine success; Compose final completion has no TC threshold.
