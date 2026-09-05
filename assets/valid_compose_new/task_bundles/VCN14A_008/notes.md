# VCN14A_008

- Instruction: Put the black bowl on the stove, then close the middle drawer of the cabinet.
- Family: `stove_placement_then_drawer_close`
- Physical group: `exact_anlgx_170__close_the_middle_drawer_of_the_wooden_cabinet`
- Semantic components: `2`
- Pure original-atomic composition: `true`

## Components

1. Put the black bowl on the stove — `on(akita_black_bowl_1, flat_stove_1_cook_region)`
2. Close the middle drawer of the cabinet — `close(wooden_cabinet_1_middle_region)`

## Notes

- Original bowl-to-stove placement precedes the exact 5/5 middle-drawer close donor.
- The complete physical scene is one evaluated donor BDDL; no entity, region, or pose is changed.
- All five serialized donor states are copied byte-for-byte.
- Success requires strict ordered native events and final BDDL goals; Compose has no final TC gate.
