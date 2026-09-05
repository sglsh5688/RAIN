# VCN10_001

- Instruction: Put the cream cheese on the stove, then push the plate to the front of the stove.
- Family: `stove_placement_then_plate_push`
- Physical group: `exact_anlgx_127__put_the_cream_cheese_on_the_stove`
- Semantic components: `2`
- Pure original-atomic composition: `true`

## Components

1. Put the cream cheese on the stove — `on(cream_cheese_1, flat_stove_1_cook_region)`
2. Push the plate to the front of the stove — `on(plate_1, main_table_stove_front_region)`

## Notes

- ANLGX_127 stove placement succeeded 3/5; the same scene already contains the original Goal push plate and destination region.
- The donor BDDL, fixture roots, object poses, articulation state and all five frozen initial states are retained exactly.
- The two goals refer only to entities and native regions already present in the single donor scene.
- Trajectory continuity is a soft empirical prior, not an exclusion rule.
- Strict ordered native events and final BDDL determine success; Compose final completion has no TC threshold.
