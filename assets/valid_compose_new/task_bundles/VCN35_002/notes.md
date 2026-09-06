# VCN35_002

- Instruction: Put the tomato sauce on the right plate, then put the ramekin in the basket.
- Family: `cylinder_to_plate_then_round_to_basket`
- Physical group: `tomato_right_plus_ramekin_basket`
- Semantic components: `2`
- Pure original-atomic composition: `false`

## Components

1. Put the tomato sauce on the right plate — `on(tomato_sauce_1,plate_2)`
2. put the ramekin in the basket — `in(glazed_rim_porcelain_ramekin_1,basket_1_contain_region)`

## Notes

- ADAPT_098 preserves the 3/5 tomato pickup/right-plate binding; WTRAYR_005 provides an exact evaluated living-room-table ramekin pickup and LBCM_003 the tabletop basket target.
- Every interacted object keeps its identity-specific official/evaluated pickup transform; basket and plate keep exact evaluated target transforms.
- All state-i entities are copied in the robot-base frame with zero deliberate offset; BDDL reset regions are not pose authority.
- The red coffee mug is removed only in ramekin scenes because attempt1 state 0 recorded 0.883–5.203 mm direct MuJoCo penetration with the exact ramekin donor pose.
- Strict two ordered native rising events and every final BDDL predicate are required; Compose completion has no final TC gate.
- A later action must preserve the earlier relation; success videos require manual downstream-preservation review before publication.
