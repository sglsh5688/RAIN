# VCN11_015

- Instruction: Put the black bowl on the stove, then close the top drawer of the wooden cabinet.
- Family: `stove_placement_then_drawer_control`
- Physical group: `exact_anlgx_169__close_the_top_drawer_of_the_wooden_cabinet`
- Semantic components: `2`
- Pure original-atomic composition: `true`

## Components

1. Put the black bowl on the stove — `on(akita_black_bowl_1, flat_stove_1_cook_region)`
2. Close the top drawer of the wooden cabinet — `close(wooden_cabinet_1_top_region)`

## Notes

- Goal bowl-to-stove was 5/5 and ANLGX_169 top close was 3/5 in this exact Goal scene.
- The donor BDDL physical scene and all five frozen initial states are retained byte-for-byte; no object, fixture, or articulation pose is edited.
- Every semantic action masks its exact manipulated object and destination; stove control is button-only, drawer control is the moving part only, and microwave insertion targets the microwave fixture.
- Gripper trajectory is a soft empirical prior, not a hard exclusion rule.
- Strict ordered native events and final BDDL determine success; Compose final completion has no TC threshold.
