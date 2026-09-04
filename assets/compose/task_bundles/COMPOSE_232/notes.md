# COMPOSE_232

- Instruction: Put the wine bottle on top of the cabinet, then push the plate to the front of the stove, then open the middle drawer of the cabinet, and finally open the top drawer and put the black bowl inside.
- Family: `X5_goal_four_task_clique`
- Physical group: `libero_goal_shared_scene_four_way`
- Semantic components: `4`
- Pure original-atomic composition: `true`

## Components

1. Put the wine bottle on top of the cabinet — `on(wine_bottle_1, wooden_cabinet_1_top_side)`
2. Push the plate to the front of the stove — `on(plate_1, main_table_stove_front_region)`
3. Open the middle drawer of the cabinet — `open(wooden_cabinet_1_middle_region)`
4. Open the top drawer and put the black bowl inside — `in(akita_black_bowl_1, wooden_cabinet_1_top_region)`

## Notes

- All six pairwise edges of Goal clique (3, 5, 6, 10) are in the audited compatibility graph.
- Goal pairs and triples were already screened in prior pools; this is the novel four-way identity.
