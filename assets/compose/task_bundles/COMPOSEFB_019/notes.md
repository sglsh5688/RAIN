# COMPOSEFB_019

- Instruction: Put the black bowl on the plate, then open the middle drawer of the right wooden cabinet, and finally put the wine bottle on top of the right wooden cabinet.
- Family: `FB2_two_cabinets_goal_exact_table_objects`
- Physical group: `feedback_kitchen4_two_cabinets_goal_exact_bowl_plate_wine`
- Semantic components: `3`
- Pure original-atomic composition: `true`

## Components

1. Put the black bowl on the plate — `on(akita_black_bowl_1, plate_1)`
2. Open the middle drawer of the right wooden cabinet — `open(wooden_cabinet_1_middle_region)`
3. Put the wine bottle on top of the right wooden cabinet — `on(wine_bottle_1, wooden_cabinet_1_top_side)`

## Notes

- The original white cabinet stays at the LIBERO-10 Kitchen Scene 4 robot-left pose.
- The wooden cabinet is at the exact LIBERO-Goal robot-right pose.
- The wine bottle is at the exact LIBERO-Goal initial pose, correcting the earlier two-cabinet screen.
- The wine rack is retained at its exact LIBERO-Goal pose as a learned-scene distractor.
- The bowl, plate, and wine bottle use their exact LIBERO-Goal initial coordinates.
- This family includes the literal plate-to-left-cabinet and wine-to-right-cabinet feedback task.
