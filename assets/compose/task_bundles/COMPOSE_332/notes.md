# COMPOSE_332

- Instruction: Open the top drawer, then put the black bowl inside the open top drawer, then close the top drawer, and finally open the middle drawer of the cabinet.
- Family: `X9_goal_open_insert_close_sequence`
- Physical group: `libero_goal_shared_scene_close_sequence`
- Semantic components: `4`
- Pure original-atomic composition: `false`

## Components

1. Open the top drawer — `open(wooden_cabinet_1_top_region)`
2. Put the black bowl inside the open top drawer — `in(akita_black_bowl_1, wooden_cabinet_1_top_region)`
3. Close the top drawer — `close(wooden_cabinet_1_top_region)`
4. Open the middle drawer of the cabinet — `open(wooden_cabinet_1_middle_region)`

## Notes

- Ordered scoring proves open top -> insert -> close top -> open middle.
