# COMPOSEFB_023

- Instruction: Put the black bowl on the plate on top of the left white cabinet, then open the middle drawer of the right wooden cabinet, and finally put the wine bottle on top of the right wooden cabinet.
- Family: `FB3_plate_preplaced_on_left_cabinet`
- Physical group: `feedback_kitchen4_two_cabinets_plate_on_left_goal_exact_bowl_wine`
- Semantic components: `3`
- Pure original-atomic composition: `true`

## Components

1. Put the black bowl on the plate on top of the left white cabinet — `on(akita_black_bowl_1, plate_1)`
2. Open the middle drawer of the right wooden cabinet — `open(wooden_cabinet_1_middle_region)`
3. Put the wine bottle on top of the right wooden cabinet — `on(wine_bottle_1, wooden_cabinet_1_top_side)`

## Notes

- The original white cabinet stays at the LIBERO-10 Kitchen Scene 4 robot-left pose.
- The wooden cabinet is at the exact LIBERO-Goal robot-right pose.
- The wine bottle is at the exact LIBERO-Goal initial pose, correcting the earlier two-cabinet screen.
- The wine rack is retained at its exact LIBERO-Goal pose as a learned-scene distractor.
- The plate starts on top of the left white cabinet, covering the alternate reading of the feedback.
- The bowl and wine bottle retain their exact LIBERO-Goal initial coordinates.
