# COMPOSEFB_008

- Instruction: Put the black bowl in the bottom drawer of the left white cabinet, then close the bottom drawer of the left white cabinet, and finally open the middle drawer of the right wooden cabinet.
- Family: `FB1_two_cabinets_goal_exact_wine`
- Physical group: `feedback_kitchen4_two_cabinets_goal_exact_wine`
- Semantic components: `3`
- Pure original-atomic composition: `true`

## Components

1. Put the black bowl in the bottom drawer of the left white cabinet — `in(akita_black_bowl_1, white_cabinet_1_bottom_region)`
2. Close the bottom drawer of the left white cabinet — `close(white_cabinet_1_bottom_region)`
3. Open the middle drawer of the right wooden cabinet — `open(wooden_cabinet_1_middle_region)`

## Notes

- The original white cabinet stays at the LIBERO-10 Kitchen Scene 4 robot-left pose.
- The wooden cabinet is at the exact LIBERO-Goal robot-right pose.
- The wine bottle is at the exact LIBERO-Goal initial pose, correcting the earlier two-cabinet screen.
- The wine rack is retained at its exact LIBERO-Goal pose as a learned-scene distractor.
- The bowl remains at the exact Kitchen Scene 4 pose to preserve its learned left-drawer trajectory.
