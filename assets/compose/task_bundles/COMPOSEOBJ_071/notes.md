# COMPOSEOBJ_071

- Instruction: Put the alphabet soup in the basket, then put the butter in the basket, then put the tomato sauce in the basket, and finally put the cream cheese box in the basket.
- Family: `L3_compose155_prefix_then_append_fourth`
- Physical group: `long_scene2_compose155_exact_states_ordered_append`
- Semantic components: `4`
- Pure original-atomic composition: `true`

## Components

1. Put the alphabet soup in the basket — `in(alphabet_soup_1, basket_1_contain_region)`
2. Put the butter in the basket — `in(butter_1, basket_1_contain_region)`
3. Put the tomato sauce in the basket — `in(tomato_sauce_1, basket_1_contain_region)`
4. Put the cream cheese box in the basket — `in(cream_cheese_1, basket_1_contain_region)`

## Notes

- Exact milk-removed COMPOSE_155 physical scene and its five init states are reused.
- The successful COMPOSE_155 prefix (alphabet soup -> butter -> tomato sauce) is completed before appending cream cheese box.
- The same unordered four-object identity previously scored 0/5; this task isolates prefix-preserving execution order.
