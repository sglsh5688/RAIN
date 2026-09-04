# COMPOSE_209

- Instruction: Put the cream cheese on the black bowl, then put the wine bottle on the rack, then push the plate to the front of the stove, and finally turn on the stove.
- Family: `X5_goal_four_task_clique`
- Physical group: `libero_goal_shared_scene_four_way`
- Semantic components: `4`
- Pure original-atomic composition: `true`

## Components

1. Put the cream cheese on the black bowl — `on(cream_cheese_1, akita_black_bowl_1)`
2. Put the wine bottle on the rack — `on(wine_bottle_1, wine_rack_1_top_region)`
3. Push the plate to the front of the stove — `on(plate_1, main_table_stove_front_region)`
4. Turn on the stove — `turnon(flat_stove_1)`

## Notes

- All six pairwise edges of Goal clique (2, 4, 6, 7) are in the audited compatibility graph.
- Goal pairs and triples were already screened in prior pools; this is the novel four-way identity.
