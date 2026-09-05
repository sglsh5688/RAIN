# VCN14A_006

- Instruction: Put the cream cheese on the black bowl, then close the middle drawer of the cabinet.
- Family: `container_placement_then_drawer_close`
- Physical group: `exact_anlgx_170__close_the_middle_drawer_of_the_wooden_cabinet`
- Semantic components: `2`
- Pure original-atomic composition: `true`

## Components

1. Put the cream cheese on the black bowl — `on(cream_cheese_1, akita_black_bowl_1)`
2. Close the middle drawer of the cabinet — `close(wooden_cabinet_1_middle_region)`

## Notes

- Cream-cheese-to-bowl precedes the 5/5 exact-donor middle-drawer close primitive.
- The complete physical scene is one evaluated donor BDDL; no entity, region, or pose is changed.
- All five serialized donor states are copied byte-for-byte.
- Success requires strict ordered native events and final BDDL goals; Compose has no final TC gate.
