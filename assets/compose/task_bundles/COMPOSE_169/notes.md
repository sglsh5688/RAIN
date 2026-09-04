# COMPOSE_169

- Instruction: Put the cream cheese box, the ketchup, and the tomato sauce in the basket one after another.
- Family: `X3_libero10_scene2_milk_removed_3_to_basket`
- Physical group: `libero10_scene2_milk_blocker_removed`
- Semantic components: `3`
- Pure original-atomic composition: `true`

## Components

1. Put the cream cheese box in the basket — `in(cream_cheese_1, basket_1_contain_region)`
2. Put the ketchup in the basket — `in(ketchup_1, basket_1_contain_region)`
3. Put the tomato sauce in the basket — `in(tomato_sauce_1, basket_1_contain_region)`

## Notes

- milk_1 and its init region are removed because prior rollouts repeatedly collided with and toppled it.
- Exhaustive C(6,3) subset after blocker removal; no instruction-order duplicates are created.
