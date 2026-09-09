# SPBSC_001

- Instruction: Put the black bowl from the top of the wooden cabinet in the basket, then put the alphabet soup in the basket.
- Family: `spatial10_bowl_then_soup_same_basket`
- Physical group: `spatial10_plate_slot_basket_cookie_slot_soup`
- Semantic components: `2`
- Pure original-atomic composition: `false`

## Components

1. Put the black bowl from the top of the wooden cabinet in the basket — `in(akita_black_bowl_1,basket_1_contain_region)`
2. Put the alphabet soup in the basket — `in(alphabet_soup_1,basket_1_contain_region)`

## Notes

- Exact LIBERO_SPATIAL_10 scene and five states. Replace only plate_1 by basket_1 at the original same-index plate XY, and cookies_1 by alphabet_soup_1 at the original same-index cookie XY. The bowl/cabinet and all unrelated retained entities keep their original poses.
- The bowl keeps its exact original LIBERO_SPATIAL_10 pickup pose; the basket replaces the original plate target slot.
- The alphabet soup replaces the original Spatial-10 cookie box at its exact same-index robot-frame XY/yaw.
- Strict ordered native rising events and both relations retained at final determine success.
- Compose has no final TC gate.
