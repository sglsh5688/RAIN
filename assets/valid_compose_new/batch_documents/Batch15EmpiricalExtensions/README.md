# Batch 15: Empirical Exact-Donor Extensions

Eleven globally novel control extensions retained from a twelve-candidate physical screen.

Original screen `VCN15_010` was excluded; original `VCN15_011` and `VCN15_012` are renumbered to final `VCN15_010` and `VCN15_011`.

| ID | Audit rank | Risk | Family | Instruction | Exact donor |
|---|---:|---|---|---|---|
| `VCN15_001` | 3 | `medium` | `stove_place_turn_then_drawer_open` | Put the cream cheese on the stove, then turn on the stove, then open the middle drawer of the wooden cabinet. | `vcn9_010__put_the_cream_cheese_on_the_stove_then_turn_on_the_stove` |
| `VCN15_002` | 4 | `medium` | `container_place_push_then_drawer_open` | Put the butter on the black bowl, then push the plate to the front of the stove, then open the middle drawer of the wooden cabinet. | `vcn11_009__put_the_butter_on_the_black_bowl_then_push_the_plate_to_the_front_of_the_stove` |
| `VCN15_003` | 5 | `medium` | `container_place_push_then_drawer_open` | Put the chocolate pudding on the black bowl, then push the plate to the front of the stove, then open the middle drawer of the wooden cabinet. | `vcn11_010__put_the_chocolate_pudding_on_the_black_bowl_then_push_the_plate_to_the_front_of_the_stove` |
| `VCN15_004` | 7 | `medium` | `moka_two_closes_then_sibling_open` | Put the moka pot on the stove, then close the middle drawer of the white cabinet, then close the bottom drawer of the white cabinet, then open the top drawer of the white cabinet. | `vcn1_014__put_the_moka_pot_on_the_stove_then_close_the_middle_drawer_of_the_white_cabinet_and_finally_close_the_bottom_drawer_of_the_white_cabinet` |
| `VCN15_005` | 8 | `medium_high` | `stove_place_push_then_turn_on` | Put the cream cheese on the stove, then push the plate to the front of the stove, then turn on the stove. | `vcn10_001__put_the_cream_cheese_on_the_stove_then_push_the_plate_to_the_front_of_the_stove` |
| `VCN15_006` | 9 | `medium_high` | `stove_place_push_then_turn_on` | Put the chocolate pudding on the stove, then push the plate to the front of the stove, then turn on the stove. | `vcn10_003__put_the_chocolate_pudding_on_the_stove_then_push_the_plate_to_the_front_of_the_stove` |
| `VCN15_007` | 17 | `high` | `stove_place_turn_then_drawer_open` | Put the chocolate pudding on the stove, then turn on the stove, then open the middle drawer of the wooden cabinet. | `vcn9_011__put_the_chocolate_pudding_on_the_stove_then_turn_on_the_stove` |
| `VCN15_008` | 18 | `high` | `container_place_push_then_turn_on` | Put the butter on the black bowl, then push the plate to the front of the stove, then turn on the stove. | `vcn11_009__put_the_butter_on_the_black_bowl_then_push_the_plate_to_the_front_of_the_stove` |
| `VCN15_009` | 19 | `high` | `container_place_push_then_turn_on` | Put the chocolate pudding on the black bowl, then push the plate to the front of the stove, then turn on the stove. | `vcn11_010__put_the_chocolate_pudding_on_the_black_bowl_then_push_the_plate_to_the_front_of_the_stove` |
| `VCN15_010` | 21 | `high` | `container_place_close_then_turn_on` | Put the chocolate pudding on the black bowl, then close the middle drawer of the wooden cabinet, then turn on the stove. | `vcn8_012__put_the_chocolate_pudding_on_the_black_bowl_then_close_the_middle_drawer_of_the_wooden_cabinet` |
| `VCN15_011` | 22 | `high` | `container_place_open_then_turn_on` | Put the chocolate pudding on the black bowl, then open the middle drawer of the cabinet, then turn on the stove. | `vcn8_008__put_the_chocolate_pudding_on_the_black_bowl_then_open_the_middle_drawer_of_the_cabinet` |

## Validation contract


- The pool is the 24 proposals in `BATCH14_EMPIRICAL_TRANSITION_AUDIT.md`. Twelve exact-scene control extensions entered the physical screen; eleven are retained. Twelve object-placement extensions are excluded because an exact original interacted pickup-slot proof is unavailable, and physical-screen candidate `VCN15_010` (audit rank 20) is excluded because opening the white middle drawer intersects `moka_pot_2` in all five donor states.
- Every retained task keeps a complete strict-success donor prefix and adds exactly one source-aligned drawer/stove control. One evaluated donor BDDL is the entire scene; no object, fixture, region, root, pose, or articulation state is edited.
- All five serialized donor states are copied byte-for-byte. Generated or resampled states are forbidden.
- Instructions contain only ordered action clauses. Wine manipulation is forbidden. Basket goals are absent (0/11, below the 25% cap).
- Every action masks its exact manipulated object and target. Drawer control selects only the requested moving part; stove control selects only `flat_stove_1_button`.
- All ordered final native predicates must be false after ten evaluator-identical wait steps. Native articulation dead-bands are allowed; no opposite-endpoint predicate is required.
- All five states must be initially and settled collision-free, all exact masks at least 10 pixels at 320x320, and all frozen replays within 1e-8 m.
- Every requested drawer/stove endpoint, including controls already in the retained prefix, must pass a full current-to-native-endpoint articulation sweep without cross-entity penetration.
- The full ordered sequence, unordered final-goal set, and semantic-alias final-goal set must be absent from every workspace `TASK_INDEX.tsv`, every workspace BDDL, all instrumented historical results, LIBERO-40, materialized/current VCN13, current Batch-14A/14B source definitions, and this batch.
- Success is strict ordered native events plus all final BDDL goals. Compose final termination has no TC threshold.
- Gripper trajectory is a soft empirical ranking prior, never a hard exclusion rule.

