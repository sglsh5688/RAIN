# VCN5_003

- Instruction: Put the moka pot on the stove, then close the bottom drawer of the white cabinet, and finally close the top drawer of the white cabinet.
- Family: `mkdc_prefix_then_top_close`
- Physical group: `vcn1_013__put_the_moka_pot_on_the_stove_then_close_the_top_drawer_of_the_white_cabinet_and_finally_close_the_bottom_drawer_of_the_white_cabinet`
- Semantic components: `3`
- Pure original-atomic composition: `true`

## Components

1. Put the moka pot on the stove — `on(moka_pot_2, flat_stove_1_cook_region)`
2. Close the bottom drawer of the white cabinet — `close(white_cabinet_1_bottom_region)`
3. Close the top drawer of the white cabinet — `close(white_cabinet_1_top_region)`

## Notes

- Exact MKDC moka/close prefix succeeded 4/5; top close is independently robust.
- The donor scene, all roots, movable poses, articulation states and all five frozen states are retained exactly.
- Trajectory continuity is a soft empirical prior, not an exclusion rule.
- Strict ordered native events determine success; Compose final termination has no TC threshold.
