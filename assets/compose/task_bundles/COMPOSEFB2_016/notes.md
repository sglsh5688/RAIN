# COMPOSEFB2_016

- Instruction: Put the plate on top of the left white cabinet, then close the bottom drawer of the left white cabinet, and finally put the wine bottle on top of the right wooden cabinet.
- Family: `FB4_full_goal_scene_plus_left_cabinet`
- Physical group: `feedback_full_goal_scene_plus_left_white_cabinet`
- Semantic components: `3`
- Pure original-atomic composition: `false`

## Components

1. Put the plate on top of the left white cabinet — `on(plate_1, white_cabinet_1_top_side)`
2. Close the bottom drawer of the left white cabinet — `close(white_cabinet_1_bottom_region)`
3. Put the wine bottle on top of the right wooden cabinet — `on(wine_bottle_1, wooden_cabinet_1_top_side)`

## Notes

- The complete LIBERO-Goal scene, table type, camera context, object set, and original coordinates are retained.
- Only the LIBERO-10 Kitchen Scene 4 white cabinet is added at its exact robot-left coordinate and yaw.
- The original Goal wooden cabinet stays at robot-right, and the wine bottle stays at its exact Goal initial coordinate.
- The plate starts at its exact original LIBERO-Goal table coordinate.
