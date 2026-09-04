# COMPOSE_285

- Instruction: Push the plate to the front of the stove, then open the middle drawer of the cabinet, and finally put the cream cheese box in the basket.
- Family: `X7_goal_plus_left_basket_3_task`
- Physical group: `libero_goal_with_robot_left_basket`
- Semantic components: `3`
- Pure original-atomic composition: `true`

## Components

1. Push the plate to the front of the stove — `on(plate_1, main_table_stove_front_region)`
2. Open the middle drawer of the cabinet — `open(wooden_cabinet_1_middle_region)`
3. Put the cream cheese box in the basket — `in(cream_cheese_1, basket_1_contain_region)`

## Notes

- One basket is added at the exact robot-left donor coordinate used by LIBERO basket scenes.
- A learned cream-cheese-to-basket primitive is composed with compatible Goal clique (6, 10).
- Goal component 4 is excluded because it assigns the same cream cheese to a conflicting final destination.
