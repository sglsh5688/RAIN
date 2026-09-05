# VCN11_004

- Instruction: Put the white porcelain mug on the plate, then put the butter to the right of the plate.
- Family: `plate_then_relative_placement`
- Physical group: `exact_adapt_168__put_the_butter_to_the_right_of_the_plate`
- Semantic components: `2`
- Pure original-atomic composition: `true`

## Components

1. Put the white porcelain mug on the plate — `on(porcelain_mug_1, plate_1)`
2. Put the butter to the right of the plate — `on(butter_1, living_room_table_plate_right_region)`

## Notes

- ADAPT_168 butter-right was 5/5; the white-mug-to-plate prefix is the original LIBERO-10 Scene-7 primitive.
- The donor BDDL physical scene and all five frozen initial states are retained byte-for-byte; no object, fixture, or articulation pose is edited.
- Every semantic action masks its exact manipulated object and destination; stove control is button-only, drawer control is the moving part only, and microwave insertion targets the microwave fixture.
- Gripper trajectory is a soft empirical prior, not a hard exclusion rule.
- Strict ordered native events and final BDDL determine success; Compose final completion has no TC threshold.
