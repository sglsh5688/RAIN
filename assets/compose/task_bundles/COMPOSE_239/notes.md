# COMPOSE_239

- Instruction: Put the cream cheese on the black bowl, then put the wine bottle on top of the cabinet, then turn on the stove, and finally open the middle drawer of the cabinet.
- Family: `X5_goal_four_task_clique`
- Physical group: `libero_goal_shared_scene_four_way`
- Semantic components: `4`
- Pure original-atomic composition: `true`

## Components

1. Put the cream cheese on the black bowl — `on(cream_cheese_1, akita_black_bowl_1)`
2. Put the wine bottle on top of the cabinet — `on(wine_bottle_1, wooden_cabinet_1_top_side)`
3. Turn on the stove — `turnon(flat_stove_1)`
4. Open the middle drawer of the cabinet — `open(wooden_cabinet_1_middle_region)`

## Notes

- All six pairwise edges of Goal clique (4, 5, 7, 10) are in the audited compatibility graph.
- Goal pairs and triples were already screened in prior pools; this is the novel four-way identity.
