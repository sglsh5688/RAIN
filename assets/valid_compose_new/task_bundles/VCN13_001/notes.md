# VCN13_001

- Instruction: Put the chocolate pudding on the black bowl, then turn on the stove.
- Family: `container_placement_then_control`
- Physical group: `exact_anlgx_139__put_the_chocolate_pudding_on_the_black_bowl`
- Semantic components: `2`
- Pure original-atomic composition: `true`

## Components

1. Put the chocolate pudding on the black bowl — `on(chocolate_pudding_1, akita_black_bowl_1)`
2. Turn on the stove — `turnon(flat_stove_1)`

## Notes

- Pudding-to-bowl was 5/5; placement-to-turn-on is an observed successful transition family.
- The complete physical scene is one evaluated donor BDDL with no pose or entity edits.
- All five serialized donor states are copied byte-for-byte.
- The additional action has explicit numeric/source pose proofs in SOURCE_COMPATIBILITY.json.
- Success is strict ordered native events plus final BDDL; Compose has no final TC gate.
