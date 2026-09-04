# COMPOSE_307

- Instruction: Put the wine bottle on the rack, then turn on the stove, then put the black bowl on the stove, and finally put the cream cheese box in the basket.
- Family: `X8_goal_plus_left_basket_4_task`
- Physical group: `libero_goal_with_robot_left_basket`
- Semantic components: `4`
- Pure original-atomic composition: `true`

## Components

1. Put the wine bottle on the rack — `on(wine_bottle_1, wine_rack_1_top_region)`
2. Turn on the stove — `turnon(flat_stove_1)`
3. Put the black bowl on the stove — `on(akita_black_bowl_1, flat_stove_1_cook_region)`
4. Put the cream cheese box in the basket — `in(cream_cheese_1, basket_1_contain_region)`

## Notes

- One basket is added at the exact robot-left donor coordinate used by LIBERO basket scenes.
- A learned cream-cheese-to-basket primitive is composed with compatible Goal clique (2, 7, 8).
- Goal component 4 is excluded because it assigns the same cream cheese to a conflicting final destination.
