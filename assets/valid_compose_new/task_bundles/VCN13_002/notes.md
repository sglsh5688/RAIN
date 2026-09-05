# VCN13_002

- Instruction: Put the white mug on the plate, then put the yellow and white mug to the right of the plate.
- Family: `plate_then_relative_placement`
- Physical group: `exact_adapt_178__put_the_yellow_and_white_mug_to_the_right_of_the_plate`
- Semantic components: `2`
- Pure original-atomic composition: `true`

## Components

1. Put the white mug on the plate — `on(porcelain_mug_1, plate_1)`
2. Put the yellow and white mug to the right of the plate — `on(white_yellow_mug_1, living_room_table_plate_right_region)`

## Notes

- The order is the original LIBERO-10 Scene-7 two-action template; the substituted right-placement atom was 4/5.
- The complete physical scene is one evaluated donor BDDL with no pose or entity edits.
- All five serialized donor states are copied byte-for-byte.
- The additional action has explicit numeric/source pose proofs in SOURCE_COMPATIBILITY.json.
- Success is strict ordered native events plus final BDDL; Compose has no final TC gate.
