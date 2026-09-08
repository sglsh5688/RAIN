# VCN91_002

- Instruction: Put the black bowl on top of the cabinet, then turn on the stove, then put the moka pot on the stove.
- Family: `k3_complete_pair_and_goal_bowl`
- Physical group: `top3`
- Semantic components: `3`
- Pure original-atomic composition: `true`

## Components

1. Put the black bowl on top of the cabinet — `on(akita_black_bowl_1,wooden_cabinet_1_top_side)`
2. Turn on the stove — `turnon(flat_stove_1)`
3. Put the moka pot on the stove — `on(moka_pot_1,flat_stove_1_cook_region)`

## Notes

- Keep original K3 stove, knob, moka pickup and robot state. Remove its frying pan; import only the complete native Goal bowl/cabinet pair into the vacated pan side by rigid robot-frame mapping.
- Preserve the entire original K3 turn-on then moka-placement pair in both block orders.
- All requested actions have explicit ordered native milestones; original terminal predicates must remain true. Open is an observed prerequisite, not an extra terminal requirement. No final TC gate.
- Initial robot/gripper contacts and articulated sweep audited; geometry clearance is not a guarantee of successful policy transfer.
