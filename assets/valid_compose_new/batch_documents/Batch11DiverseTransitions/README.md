# Batch 11: Diverse Transitions

Fifteen two-step Compose probes built from exact five-state donors. See `TASK_INDEX.tsv` for the full machine-readable inventory and `PROVENANCE.tsv` for donor/evidence details.

| ID | Family | Instruction | Donor |
|---|---|---|---|
| `VCN11_001` | `two_front_plate_placements` | Put the cream cheese on the left front plate, then put the yellow and white mug on the right front plate. | `adapt_089__put_the_cream_cheese_on_the_left_front_plate` |
| `VCN11_002` | `two_front_plate_placements` | Put the milk on the left front plate, then put the yellow and white mug on the right front plate. | `adapt_101__put_the_milk_on_the_left_front_plate` |
| `VCN11_003` | `two_front_plate_placements` | Put the bbq sauce on the left front plate, then put the yellow and white mug on the right front plate. | `adapt_093__put_the_bbq_sauce_on_the_left_front_plate` |
| `VCN11_004` | `plate_then_relative_placement` | Put the white porcelain mug on the plate, then put the butter to the right of the plate. | `adapt_168__put_the_butter_to_the_right_of_the_plate` |
| `VCN11_005` | `plate_then_relative_placement` | Put the white porcelain mug on the plate, then put the cream cheese to the right of the plate. | `adapt_158__put_the_cream_cheese_to_the_right_of_the_plate` |
| `VCN11_006` | `plate_then_relative_placement` | Put the white porcelain mug on the plate, then put the bbq sauce to the right of the plate. | `adapt_162__put_the_bbq_sauce_to_the_right_of_the_plate` |
| `VCN11_007` | `two_objects_distinct_caddy_compartments` | Put the bbq sauce in the back compartment of the caddy, then put the yellow and white mug in the left compartment of the caddy. | `adapt_121__put_the_bbq_sauce_in_the_back_compartment_of_the_caddy` |
| `VCN11_008` | `two_objects_distinct_caddy_compartments` | Put the salad dressing in the back compartment of the caddy, then put the yellow and white mug in the left compartment of the caddy. | `adapt_117__put_the_salad_dressing_in_the_back_compartment_of_the_caddy` |
| `VCN11_009` | `container_placement_then_push` | Put the butter on the black bowl, then push the plate to the front of the stove. | `anlgx_138__put_the_butter_on_the_black_bowl` |
| `VCN11_010` | `container_placement_then_push` | Put the chocolate pudding on the black bowl, then push the plate to the front of the stove. | `anlgx_139__put_the_chocolate_pudding_on_the_black_bowl` |
| `VCN11_011` | `cabinet_placement_then_push` | Put the butter on the top of the wooden cabinet, then push the plate to the front of the stove. | `anlgx_136__put_the_butter_on_the_top_of_the_wooden_cabinet` |
| `VCN11_012` | `container_placement_then_stove_control` | Put the butter on the black bowl, then turn on the stove. | `anlgx_138__put_the_butter_on_the_black_bowl` |
| `VCN11_013` | `plate_placement_then_stove_control` | Put the chocolate pudding on the plate, then turn on the stove. | `anlgx_143__put_the_chocolate_pudding_on_the_plate` |
| `VCN11_014` | `push_then_drawer_control` | Push the plate to the front of the stove, then close the top drawer of the wooden cabinet. | `anlgx_169__close_the_top_drawer_of_the_wooden_cabinet` |
| `VCN11_015` | `stove_placement_then_drawer_control` | Put the black bowl on the stove, then close the top drawer of the wooden cabinet. | `anlgx_169__close_the_top_drawer_of_the_wooden_cabinet` |

## Validation


- Fifteen candidates use one evaluated donor BDDL and its five frozen states byte-for-byte. No fixture, object, or articulation pose is changed.
- Every task has exactly two strict ordered native events and two final BDDL predicates.
- Final Compose termination is ordered native goals plus final BDDL only; there is no final TC threshold.
- Each semantic manipulation binds its exact object and target. Stove control masks only `flat_stove_1_button`; wooden-drawer control masks only `wooden_cabinet_1:top`.
- Initial native goals must all be false after the evaluator's ten wait steps. Drawer-close tasks retain the exact partially-open atomic donor state and must pass a full native close sweep; they need not satisfy the stricter native `Open` threshold.
- Every state must have no initial/settled cross-entity penetration, all mask areas at least 10 pixels at 320x320, an exact second replay within 1e-8 m, and a unique frozen-state hash.
- Drawer-close candidates must pass a full initial-to-native-close sweep with no cross-entity penetration and a true native `Close` endpoint.
- Ordered sequences and unordered final-goal sets are rejected if they overlap LIBERO-40, selected Compose, or VCN Batch 1-10. Internal ordered and final-set duplicates are also rejected.
- Gripper trajectory continuity is recorded as a soft empirical prior, not a hard exclusion rule.

