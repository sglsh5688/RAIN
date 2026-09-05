# Batch 14B: Placement Transitions

Fifteen globally novel, basket-free two-step Compose probes retained after the original twenty-candidate five-state physical screen.

| Retained ID | Original screen ID | Family | Risk | Instruction | Exact donor |
|---|---|---|---|---|---|
| `VCN14B_001` | `VCN14B_002` | `two_objects_distinct_caddy_compartments` | `medium` | Put the alphabet soup in the back compartment of the caddy, then put the yellow and white mug in the left compartment of the caddy. | `adapt_113__put_the_alphabet_soup_in_the_back_compartment_of_the_caddy` |
| `VCN14B_002` | `VCN14B_003` | `two_objects_distinct_caddy_compartments` | `medium` | Put the ketchup in the back compartment of the caddy, then put the yellow and white mug in the left compartment of the caddy. | `adapt_125__put_the_ketchup_in_the_back_compartment_of_the_caddy` |
| `VCN14B_003` | `VCN14B_004` | `two_objects_distinct_caddy_compartments` | `medium` | Put the orange juice in the back compartment of the caddy, then put the yellow and white mug in the left compartment of the caddy. | `adapt_141__put_the_orange_juice_in_the_back_compartment_of_the_caddy` |
| `VCN14B_004` | `VCN14B_005` | `nested_container_then_container_transfer` | `medium` | Put the butter on the black bowl, then put the black bowl on the stove. | `anlgx_138__put_the_butter_on_the_black_bowl` |
| `VCN14B_005` | `VCN14B_006` | `nested_container_then_container_transfer` | `medium` | Put the chocolate pudding on the black bowl, then put the black bowl on the stove. | `anlgx_139__put_the_chocolate_pudding_on_the_black_bowl` |
| `VCN14B_006` | `VCN14B_007` | `cabinet_placement_then_container_placement` | `medium` | Put the plate on the top of the wooden cabinet, then put the cream cheese on the black bowl. | `anlgx_134__put_the_plate_on_the_top_of_the_wooden_cabinet` |
| `VCN14B_007` | `VCN14B_008` | `cabinet_placement_then_container_placement` | `low` | Put the butter on the top of the wooden cabinet, then put the cream cheese on the black bowl. | `anlgx_136__put_the_butter_on_the_top_of_the_wooden_cabinet` |
| `VCN14B_008` | `VCN14B_009` | `cabinet_placement_then_container_placement` | `medium` | Put the chocolate pudding on the top of the wooden cabinet, then put the cream cheese on the black bowl. | `anlgx_137__put_the_chocolate_pudding_on_the_top_of_the_wooden_cabinet` |
| `VCN14B_009` | `VCN14B_012` | `stove_placement_then_stove_front_push` | `medium` | Put the moka pot on the stove, then push the plate to the front of the stove. | `adaptx_003__put_the_moka_pot_on_the_stove` |
| `VCN14B_010` | `VCN14B_013` | `drawer_extraction_then_same_drawer_close` | `medium` | Pick up the ramekin in the top drawer of the wooden cabinet and place it on the plate, then close the top drawer of the wooden cabinet. | `anlgx_094__pick_up_the_ramekin_in_the_top_drawer_of_the_wooden_cabinet_and_place_it_on_the_plate` |
| `VCN14B_011` | `VCN14B_014` | `stove_to_plate_then_drawer_open` | `high` | Pick up the cookies box on the stove and place it on the plate, then open the middle drawer of the wooden cabinet. | `anlgx_103__pick_up_the_cookies_box_on_the_stove_and_place_it_on_the_plate` |
| `VCN14B_012` | `VCN14B_016` | `stove_to_plate_then_drawer_open` | `medium` | Pick up the chocolate pudding on the stove and place it on the plate, then open the middle drawer of the wooden cabinet. | `anlgx_107__pick_up_the_chocolate_pudding_on_the_stove_and_place_it_on_the_plate` |
| `VCN14B_013` | `VCN14B_017` | `drawer_insertion_then_stove_front_push` | `medium` | Put the cream cheese in the top drawer of the wooden cabinet, then push the plate to the front of the stove. | `anlgx_147__put_the_cream_cheese_in_the_top_drawer_of_the_wooden_cabinet` |
| `VCN14B_014` | `VCN14B_018` | `drawer_insertion_then_stove_front_push` | `medium` | Put the butter in the top drawer of the wooden cabinet, then push the plate to the front of the stove. | `anlgx_150__put_the_butter_in_the_top_drawer_of_the_wooden_cabinet` |
| `VCN14B_015` | `VCN14B_019` | `drawer_insertion_then_stove_front_push` | `medium` | Put the chocolate pudding in the top drawer of the wooden cabinet, then push the plate to the front of the stove. | `anlgx_153__put_the_chocolate_pudding_in_the_top_drawer_of_the_wooden_cabinet` |

## Excluded by the physical screen

Source: `LIBERO_EX_ICRA27/LiberoValidComposeNew20260905/BATCH14B_PHYSICAL_SCREEN.json` (`3a22be81bdc93123f6262d56b01a1b10b35483957b9d85a98ace1ffec909fce2`).

| Original ID | Instruction | Physical exclusion |
|---|---|---|
| `VCN14B_001` | Put the white porcelain mug on the plate, then put the ketchup to the right of the plate. | State 3 had the second ordered final goal true initially, so the all-final-goals-false hard gate failed. |
| `VCN14B_010` | Put the yellow and white mug in the microwave, then turn on the stove. | All five states had initial and settled white_yellow_mug_1-to-microwave_1 penetration. |
| `VCN14B_011` | Put the yellow and white mug in the microwave, then push the plate to the front of the stove. | All five states had initial and settled white_yellow_mug_1-to-microwave_1 penetration; state 4 also had a 6-pixel plate mask below the 10-pixel gate. |
| `VCN14B_015` | Pick up the ramekin on the stove and place it on the plate, then open the middle drawer of the wooden cabinet. | All five states had approximately 1.51 mm ramekin-to-flat-stove penetration in the initial, settled, and articulation-sweep checks. |
| `VCN14B_020` | Put the chocolate pudding in the bottom drawer of the wooden cabinet, then turn on the stove. | States 3 and 4 had initial chocolate-pudding-to-wooden-cabinet penetration; state 4 additionally settled with plate-to-cabinet penetration. |

## Validation contract


- Every task has exactly two action-only clauses and uses one previously evaluated atomic donor BDDL as the complete scene.
- The donor BDDL and all five serialized donor states are retained byte-for-byte; no object, fixture, region, or articulation pose is synthesized.
- Basket goals are excluded. Wine bottles may remain unchanged distractors but are never manipulated.
- Ordered sequence, unordered final-goal set, and semantic-alias final-goal set must be absent from LIBERO-40, selected/historical workspace tasks and results, every VCN Batch 1--13 source definition, and this batch.
- Every action masks its exact manipulated object and target. Stove control masks only `flat_stove_1_button`; drawer control masks only the corresponding moving drawer part; microwave insertion targets only `microwave_1`; push targets only the exact stove-front region.
- All final goals must be false after the evaluator-identical ten wait steps. Every state must have no initial/settled cross-entity penetration, every exact mask must cover at least 10 pixels at 320x320, and frozen replay body error must be at most 1e-8 m.
- A middle-drawer-open action additionally requires a sweep from the actual settled initial joint value to the native `Open` endpoint without cross-entity penetration. The initial value may lie in the articulation dead-band; native `Close` is not required.
- Retained `VCN14B_010` (original physical-screen ID `VCN14B_013`) closes the same top drawer only after its first action removes the ramekin. Its dependent close sweep must therefore be interpreted at the post-prefix state during rollout review; no initial-state shortcut is accepted.
- Caddy suffixes retain the donor-native yellow-mug pose. Their caddy fixture/target geometry is exact, but the pickup transition is intentionally a medium-risk soft-trajectory probe.
- Gripper trajectory is a soft empirical prior, not a hard exclusion rule.
- Success is strict ordered native events plus final BDDL goals. Compose final termination has no TC threshold.

