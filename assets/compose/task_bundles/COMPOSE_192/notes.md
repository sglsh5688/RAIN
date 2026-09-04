# COMPOSE_192

- Instruction: Put the black bowl on the plate, then put the wine bottle on the rack, then turn on the stove, and finally open the middle drawer of the cabinet.
- Family: `X5_goal_four_task_clique`
- Physical group: `libero_goal_shared_scene_four_way`
- Semantic components: `4`
- Pure original-atomic composition: `true`

## Components

1. Put the black bowl on the plate — `on(akita_black_bowl_1, plate_1)`
2. Put the wine bottle on the rack — `on(wine_bottle_1, wine_rack_1_top_region)`
3. Turn on the stove — `turnon(flat_stove_1)`
4. Open the middle drawer of the cabinet — `open(wooden_cabinet_1_middle_region)`

## Notes

- All six pairwise edges of Goal clique (1, 2, 7, 10) are in the audited compatibility graph.
- Goal pairs and triples were already screened in prior pools; this is the novel four-way identity.
