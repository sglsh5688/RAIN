# VCN13_010

- Instruction: Put the white mug on the plate, then put the tomato sauce to the right of the plate.
- Family: `plate_then_relative_placement`
- Physical group: `exact_adapt_166__put_the_tomato_sauce_to_the_right_of_the_plate`
- Semantic components: `2`
- Pure original-atomic composition: `true`

## Components

1. Put the white mug on the plate — `on(porcelain_mug_1, plate_1)`
2. Put the tomato sauce to the right of the plate — `on(tomato_sauce_1, living_room_table_plate_right_region)`

## Notes

- The order is the original Scene-7 template; tomato-right was 2/5.
- The complete physical scene is one evaluated donor BDDL with no pose or entity edits.
- All five serialized donor states are copied byte-for-byte.
- The additional action has explicit numeric/source pose proofs in SOURCE_COMPATIBILITY.json.
- Success is strict ordered native events plus final BDDL; Compose has no final TC gate.
