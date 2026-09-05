# COMPOSEOBJ_256

- Instruction: Put the tomato sauce in the basket, then put the butter in the basket, and finally put the bbq sauce in the basket.
- Family: `O2_object_milk_upper_swap_3_to_basket`
- Physical group: `object_milk_upper_swap_pick_up_the_tomato_sauce_and_place_it_in_the_basket`
- Semantic components: `3`
- Pure original-atomic composition: `true`

## Components

1. Put the tomato sauce in the basket — `in(tomato_sauce_1, basket_1_contain_region)`
2. Put the butter in the basket — `in(butter_1, basket_1_contain_region)`
3. Put the bbq sauce in the basket — `in(bbq_sauce_1, basket_1_contain_region)`

## Notes

- Milk is swapped into floor_other_object_region_1 (the upper/back slot); butter_1 moves to milk's former floor_other_object_region_0 slot.
- The five non-milk objects and basket remain exactly the same identities as the source Object scene.
