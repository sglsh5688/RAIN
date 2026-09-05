# VCN14A_005

- Instruction: Put the cream cheese on the black bowl, then close the top drawer of the cabinet.
- Family: `container_placement_then_drawer_close`
- Physical group: `exact_anlgx_169__close_the_top_drawer_of_the_wooden_cabinet`
- Semantic components: `2`
- Pure original-atomic composition: `true`

## Components

1. Put the cream cheese on the black bowl — `on(cream_cheese_1, akita_black_bowl_1)`
2. Close the top drawer of the cabinet — `close(wooden_cabinet_1_top_region)`

## Notes

- The exact ANLGX_169 scene supplies a physically open top drawer and a 3/5 close primitive.
- The complete physical scene is one evaluated donor BDDL; no entity, region, or pose is changed.
- All five serialized donor states are copied byte-for-byte.
- Success requires strict ordered native events and final BDDL goals; Compose has no final TC gate.
