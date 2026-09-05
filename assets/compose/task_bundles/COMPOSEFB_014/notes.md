# COMPOSEFB_014

- Instruction: Put the plate on top of the left white cabinet, then close the bottom drawer of the left white cabinet, and finally put the wine bottle on top of the right wooden cabinet.
- Family: `FB2_two_cabinets_goal_exact_table_objects`
- Physical group: `feedback_kitchen4_two_cabinets_goal_exact_bowl_plate_wine`
- Semantic components: `3`
- Pure original-atomic composition: `false`

## Components

1. Put the plate on top of the left white cabinet — `on(plate_1, white_cabinet_1_top_side)`
2. Close the bottom drawer of the left white cabinet — `close(white_cabinet_1_bottom_region)`
3. Put the wine bottle on top of the right wooden cabinet — `on(wine_bottle_1, wooden_cabinet_1_top_side)`

## Notes

- The original white cabinet stays at the LIBERO-10 Kitchen Scene 4 robot-left pose.
- The wooden cabinet is at the exact LIBERO-Goal robot-right pose.
- The wine bottle is at the exact LIBERO-Goal initial pose, correcting the earlier two-cabinet screen.
- The wine rack is retained at its exact LIBERO-Goal pose as a learned-scene distractor.
- The bowl, plate, and wine bottle use their exact LIBERO-Goal initial coordinates.
- This family includes the literal plate-to-left-cabinet and wine-to-right-cabinet feedback task.
