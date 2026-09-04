# COMPOSE_314

- Instruction: Put the wine bottle on top of the cabinet, then open the middle drawer of the cabinet, then open the top drawer and put the black bowl inside, and finally put the cream cheese box in the basket.
- Family: `X8_goal_plus_left_basket_4_task`
- Physical group: `libero_goal_with_robot_left_basket`
- Semantic components: `4`
- Pure original-atomic composition: `true`

## Components

1. Put the wine bottle on top of the cabinet — `on(wine_bottle_1, wooden_cabinet_1_top_side)`
2. Open the middle drawer of the cabinet — `open(wooden_cabinet_1_middle_region)`
3. Open the top drawer and put the black bowl inside — `in(akita_black_bowl_1, wooden_cabinet_1_top_region)`
4. Put the cream cheese box in the basket — `in(cream_cheese_1, basket_1_contain_region)`

## Notes

- One basket is added at the exact robot-left donor coordinate used by LIBERO basket scenes.
- A learned cream-cheese-to-basket primitive is composed with compatible Goal clique (3, 5, 10).
- Goal component 4 is excluded because it assigns the same cream cheese to a conflicting final destination.
