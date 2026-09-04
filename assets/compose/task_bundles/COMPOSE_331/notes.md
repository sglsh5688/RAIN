# COMPOSE_331

- Instruction: Open the top drawer, then put the black bowl inside the open top drawer, and finally close the top drawer.
- Family: `X9_goal_open_insert_close_sequence`
- Physical group: `libero_goal_shared_scene_close_sequence`
- Semantic components: `3`
- Pure original-atomic composition: `false`

## Components

1. Open the top drawer — `open(wooden_cabinet_1_top_region)`
2. Put the black bowl inside the open top drawer — `in(akita_black_bowl_1, wooden_cabinet_1_top_region)`
3. Close the top drawer — `close(wooden_cabinet_1_top_region)`

## Notes

- Ordered scoring proves open -> insert -> close; a final closed drawer alone cannot satisfy the task.
