# COMPOSE_252

- Instruction: Push the plate to the front of the stove, then turn on the stove, then open the middle drawer of the cabinet, and finally put the black bowl on the stove.
- Family: `X5_goal_four_task_clique`
- Physical group: `libero_goal_shared_scene_four_way`
- Semantic components: `4`
- Pure original-atomic composition: `true`

## Components

1. Push the plate to the front of the stove — `on(plate_1, main_table_stove_front_region)`
2. Turn on the stove — `turnon(flat_stove_1)`
3. Open the middle drawer of the cabinet — `open(wooden_cabinet_1_middle_region)`
4. Put the black bowl on the stove — `on(akita_black_bowl_1, flat_stove_1_cook_region)`

## Notes

- All six pairwise edges of Goal clique (6, 7, 8, 10) are in the audited compatibility graph.
- Goal pairs and triples were already screened in prior pools; this is the novel four-way identity.
