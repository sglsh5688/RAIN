# COMPOSE_159

- Instruction: Put the alphabet soup, the ketchup, and the orange juice in the basket one after another.
- Family: `X3_libero10_scene2_milk_removed_3_to_basket`
- Physical group: `libero10_scene2_milk_blocker_removed`
- Semantic components: `3`
- Pure original-atomic composition: `true`

## Components

1. Put the alphabet soup in the basket — `in(alphabet_soup_1, basket_1_contain_region)`
2. Put the ketchup in the basket — `in(ketchup_1, basket_1_contain_region)`
3. Put the orange juice in the basket — `in(orange_juice_1, basket_1_contain_region)`

## Notes

- milk_1 and its init region are removed because prior rollouts repeatedly collided with and toppled it.
- Exhaustive C(6,3) subset after blocker removal; no instruction-order duplicates are created.
