# VCN14A_010

- Instruction: Put the cream cheese on the plate, then turn on the stove.
- Family: `plate_placement_then_stove_control`
- Physical group: `exact_anlgx_141__put_the_cream_cheese_on_the_plate`
- Semantic components: `2`
- Pure original-atomic composition: `true`

## Components

1. Put the cream cheese on the plate — `on(cream_cheese_1, plate_1)`
2. Turn on the stove — `turnon(flat_stove_1)`

## Notes

- Cream-cheese-to-plate was 1/5; placement-to-turn is an observed partially successful transition family.
- The complete physical scene is one evaluated donor BDDL; no entity, region, or pose is changed.
- All five serialized donor states are copied byte-for-byte.
- Success requires strict ordered native events and final BDDL goals; Compose has no final TC gate.
