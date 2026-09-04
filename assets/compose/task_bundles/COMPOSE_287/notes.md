# COMPOSE_287

- Instruction: Turn on the stove, then put the black bowl on top of the cabinet, and finally put the cream cheese box in the basket.
- Family: `X7_goal_plus_left_basket_3_task`
- Physical group: `libero_goal_with_robot_left_basket`
- Semantic components: `3`
- Pure original-atomic composition: `true`

## Components

1. Turn on the stove — `turnon(flat_stove_1)`
2. Put the black bowl on top of the cabinet — `on(akita_black_bowl_1, wooden_cabinet_1_top_side)`
3. Put the cream cheese box in the basket — `in(cream_cheese_1, basket_1_contain_region)`

## Notes

- One basket is added at the exact robot-left donor coordinate used by LIBERO basket scenes.
- A learned cream-cheese-to-basket primitive is composed with compatible Goal clique (7, 9).
- Goal component 4 is excluded because it assigns the same cream cheese to a conflicting final destination.
