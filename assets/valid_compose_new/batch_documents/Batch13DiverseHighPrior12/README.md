# Batch 13: Diverse High-Priority Exact Donors

Twelve two-step candidates retained after static and five-state physical screening.

| ID | Proposal | Family | Instruction | Exact donor |
|---|---|---|---|---|
| `VCN13_001` | `P21` | `container_placement_then_control` | Put the chocolate pudding on the black bowl, then turn on the stove. | `anlgx_139__put_the_chocolate_pudding_on_the_black_bowl` |
| `VCN13_002` | `P04` | `plate_then_relative_placement` | Put the white mug on the plate, then put the yellow and white mug to the right of the plate. | `adapt_178__put_the_yellow_and_white_mug_to_the_right_of_the_plate` |
| `VCN13_003` | `P05` | `plate_then_relative_placement` | Put the white mug on the plate, then put the alphabet soup to the right of the plate. | `adapt_156__put_the_alphabet_soup_to_the_right_of_the_plate` |
| `VCN13_004` | `P01` | `two_front_plate_placements` | Put the chocolate pudding on the left front plate, then put the yellow and white mug on the right front plate. | `adapt_103__put_the_chocolate_pudding_on_the_left_front_plate` |
| `VCN13_005` | `P19` | `cabinet_placement_then_push` | Put the cream cheese on the top of the wooden cabinet, then push the plate to the front of the stove. | `anlgx_135__put_the_cream_cheese_on_the_top_of_the_wooden_cabinet` |
| `VCN13_006` | `P18` | `cabinet_placement_then_push` | Put the chocolate pudding on the top of the wooden cabinet, then push the plate to the front of the stove. | `anlgx_137__put_the_chocolate_pudding_on_the_top_of_the_wooden_cabinet` |
| `VCN13_007` | `P22` | `cabinet_placement_then_sibling_open` | Put the chocolate pudding on the top of the wooden cabinet, then open the middle drawer of the cabinet. | `anlgx_137__put_the_chocolate_pudding_on_the_top_of_the_wooden_cabinet` |
| `VCN13_008` | `P23` | `cabinet_placement_then_control` | Put the cream cheese on the top of the wooden cabinet, then turn on the stove. | `anlgx_135__put_the_cream_cheese_on_the_top_of_the_wooden_cabinet` |
| `VCN13_009` | `P24` | `cabinet_placement_then_control` | Put the chocolate pudding on the top of the wooden cabinet, then turn on the stove. | `anlgx_137__put_the_chocolate_pudding_on_the_top_of_the_wooden_cabinet` |
| `VCN13_010` | `P07` | `plate_then_relative_placement` | Put the white mug on the plate, then put the tomato sauce to the right of the plate. | `adapt_166__put_the_tomato_sauce_to_the_right_of_the_plate` |
| `VCN13_011` | `P02` | `two_front_plate_placements` | Put the tomato sauce on the left front plate, then put the yellow and white mug on the right front plate. | `adapt_097__put_the_tomato_sauce_on_the_left_front_plate` |
| `VCN13_012` | `P03` | `two_front_plate_placements` | Put the butter on the left front plate, then put the yellow and white mug on the right front plate. | `adapt_099__put_the_butter_on_the_left_front_plate` |

## Validation


- Each task uses one already evaluated donor BDDL as its entire physical scene and copies that donor's five serialized states byte-for-byte. No fixture, object, region, or pose is synthesized.
- Every task has exactly two action-only clauses, two strict ordered native events, and two final BDDL predicates.
- Final Compose termination is ordered native goals plus final BDDL only. There is no final TC threshold.
- Every action binds the exact manipulated object and target. Stove control masks only `flat_stove_1_button`; middle-drawer control masks only `wooden_cabinet_1:middle`.
- The additional action's object/fixture support region and every explicit target region must numerically match a learned or successfully evaluated source BDDL. These proofs are stored in `SOURCE_COMPATIBILITY.json`.
- All native goals must be false after the evaluator-identical ten wait steps. Exact donor states may remain in an articulation predicate dead-band; the endpoint sweep separately proves reachability.
- Every state must have empty initial/settled cross-entity penetration, every exact mask at least 10 pixels at 320x320, and a second frozen replay within 1e-8 m.
- A middle-drawer action must pass a complete initial-to-native-open sweep with no cross-entity penetration and a true native `Open` endpoint.
- Ordered sequence, unordered final-goal set, and semantic-alias final-goal set must be absent from all workspace TASK_INDEX files, BDDLs, instrumented result files, LIBERO-40, VCN Batch 11 source definitions, Batch 12's two retained source definitions, and this batch's other candidates.
- Gripper trajectory is a soft empirical prior, not a hard exclusion rule.

