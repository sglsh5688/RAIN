# COMPOSE_242

- Instruction: Put the cream cheese on the black bowl, then push the plate to the front of the stove, then turn on the stove, and finally put the black bowl on top of the cabinet.
- Family: `X5_goal_four_task_clique`
- Physical group: `libero_goal_shared_scene_four_way`
- Semantic components: `4`
- Pure original-atomic composition: `true`

## Components

1. Put the cream cheese on the black bowl — `on(cream_cheese_1, akita_black_bowl_1)`
2. Push the plate to the front of the stove — `on(plate_1, main_table_stove_front_region)`
3. Turn on the stove — `turnon(flat_stove_1)`
4. Put the black bowl on top of the cabinet — `on(akita_black_bowl_1, wooden_cabinet_1_top_side)`

## Notes

- All six pairwise edges of Goal clique (4, 6, 7, 9) are in the audited compatibility graph.
- Goal pairs and triples were already screened in prior pools; this is the novel four-way identity.
