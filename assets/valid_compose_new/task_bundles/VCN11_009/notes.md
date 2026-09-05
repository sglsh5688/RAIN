# VCN11_009

- Instruction: Put the butter on the black bowl, then push the plate to the front of the stove.
- Family: `container_placement_then_push`
- Physical group: `exact_anlgx_138__put_the_butter_on_the_black_bowl`
- Semantic components: `2`
- Pure original-atomic composition: `true`

## Components

1. Put the butter on the black bowl — `on(butter_1, akita_black_bowl_1)`
2. Push the plate to the front of the stove — `on(plate_1, main_table_stove_front_region)`

## Notes

- ANLGX_138 butter-to-bowl was 5/5; the retained plate and stove-front region are the original Goal push geometry.
- The donor BDDL physical scene and all five frozen initial states are retained byte-for-byte; no object, fixture, or articulation pose is edited.
- Every semantic action masks its exact manipulated object and destination; stove control is button-only, drawer control is the moving part only, and microwave insertion targets the microwave fixture.
- Gripper trajectory is a soft empirical prior, not a hard exclusion rule.
- Strict ordered native events and final BDDL determine success; Compose final completion has no TC threshold.
