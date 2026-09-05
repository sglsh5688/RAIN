# VCN14A_009

- Instruction: Put the black bowl on top of the cabinet, then close the top drawer of the cabinet.
- Family: `cabinet_placement_then_drawer_close`
- Physical group: `exact_anlgx_169__close_the_top_drawer_of_the_wooden_cabinet`
- Semantic components: `2`
- Pure original-atomic composition: `true`

## Components

1. Put the black bowl on top of the cabinet — `on(akita_black_bowl_1, wooden_cabinet_1_top_side)`
2. Close the top drawer of the cabinet — `close(wooden_cabinet_1_top_region)`

## Notes

- Original bowl-to-cabinet placement precedes the exact top-drawer close donor.
- The complete physical scene is one evaluated donor BDDL; no entity, region, or pose is changed.
- All five serialized donor states are copied byte-for-byte.
- Success requires strict ordered native events and final BDDL goals; Compose has no final TC gate.
