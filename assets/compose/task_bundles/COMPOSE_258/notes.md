# COMPOSE_258

- Instruction: Push the plate to the front of the stove, and then put the cream cheese box in the basket.
- Family: `X6_goal_plus_left_basket_2_task`
- Physical group: `libero_goal_with_robot_left_basket`
- Semantic components: `2`
- Pure original-atomic composition: `true`

## Components

1. Push the plate to the front of the stove — `on(plate_1, main_table_stove_front_region)`
2. Put the cream cheese box in the basket — `in(cream_cheese_1, basket_1_contain_region)`

## Notes

- One basket is added at the exact robot-left donor coordinate used by LIBERO basket scenes.
- A learned cream-cheese-to-basket primitive is composed with compatible Goal clique (6,).
- Goal component 4 is excluded because it assigns the same cream cheese to a conflicting final destination.
