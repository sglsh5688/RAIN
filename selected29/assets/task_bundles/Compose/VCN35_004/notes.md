# VCN35_004

- Instruction: Put the ramekin in the basket, then put the alphabet soup on the right plate.
- Family: `round_to_basket_then_cylinder_to_plate`
- Physical group: `soup_right_plus_ramekin_basket`
- Semantic components: `2`
- Pure original-atomic composition: `false`

## Components

1. Put the ramekin in the basket — `in(glazed_rim_porcelain_ramekin_1,basket_1_contain_region)`
2. put the alphabet soup on the right plate — `on(alphabet_soup_1,plate_2)`

## Notes

- WTRAYR_005 provides the exact living-room-table ramekin pickup (with ANLGX_088 identity evidence); ADAPT_088 preserves the 4/5 soup pickup/right-plate binding.
- Every interacted object keeps its identity-specific official/evaluated pickup transform; basket and plate keep exact evaluated target transforms.
- All state-i entities are copied in the robot-base frame with zero deliberate offset; BDDL reset regions are not pose authority.
- The red coffee mug is removed only in ramekin scenes because attempt1 state 0 recorded 0.883–5.203 mm direct MuJoCo penetration with the exact ramekin donor pose.
- Strict two ordered native rising events and every final BDDL predicate are required; Compose completion has no final TC gate.
- A later action must preserve the earlier relation; success videos require manual downstream-preservation review before publication.
