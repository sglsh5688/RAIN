# COMPOSE_247

- Instruction: Put the cream cheese on the black bowl, then turn on the stove, then open the middle drawer of the cabinet, and finally put the black bowl on top of the cabinet.
- Family: `X5_goal_four_task_clique`
- Physical group: `libero_goal_shared_scene_four_way`
- Semantic components: `4`
- Pure original-atomic composition: `true`

## Components

1. Put the cream cheese on the black bowl — `on(cream_cheese_1, akita_black_bowl_1)`
2. Turn on the stove — `turnon(flat_stove_1)`
3. Open the middle drawer of the cabinet — `open(wooden_cabinet_1_middle_region)`
4. Put the black bowl on top of the cabinet — `on(akita_black_bowl_1, wooden_cabinet_1_top_side)`

## Notes

- All six pairwise edges of Goal clique (4, 7, 9, 10) are in the audited compatibility graph.
- Goal pairs and triples were already screened in prior pools; this is the novel four-way identity.
