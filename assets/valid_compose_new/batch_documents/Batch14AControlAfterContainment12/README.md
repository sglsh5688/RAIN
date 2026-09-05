# Batch 14A: Control After Containment / Placement

Twelve globally novel two-step Compose probes retained after a strict five-state physical screen.

| Retained ID | Original screen ID | Family | Instruction | Exact donor | Atomic evidence |
|---|---|---|---|---|---|
| `VCN14A_001` | `VCN14A_001` | `container_placement_then_sibling_open` | Put the butter on the black bowl, then open the top drawer of the cabinet. | `anlgx_138__put_the_butter_on_the_black_bowl` | butter_bowl=5/5; open_top=3/5 atomic sibling |
| `VCN14A_002` | `VCN14A_003` | `cabinet_placement_then_drawer_open` | Put the cream cheese on the top of the wooden cabinet, then open the top drawer of the cabinet. | `anlgx_135__put_the_cream_cheese_on_the_top_of_the_wooden_cabinet` | cheese_cabinet=2/5; open_top=3/5 atomic sibling |
| `VCN14A_003` | `VCN14A_004` | `cabinet_placement_then_drawer_open` | Put the butter on the top of the wooden cabinet, then open the middle drawer of the cabinet. | `anlgx_136__put_the_butter_on_the_top_of_the_wooden_cabinet` | butter_cabinet=4/5; open_middle=original LIBERO-Goal |
| `VCN14A_004` | `VCN14A_005` | `plate_placement_then_drawer_open` | Put the chocolate pudding on the plate, then open the top drawer of the cabinet. | `anlgx_143__put_the_chocolate_pudding_on_the_plate` | pudding_plate=2/5; open_top=3/5 atomic sibling |
| `VCN14A_005` | `VCN14A_007` | `container_placement_then_drawer_close` | Put the cream cheese on the black bowl, then close the top drawer of the cabinet. | `anlgx_169__close_the_top_drawer_of_the_wooden_cabinet` | cheese_bowl=original LIBERO-Goal; close_top=3/5 |
| `VCN14A_006` | `VCN14A_008` | `container_placement_then_drawer_close` | Put the cream cheese on the black bowl, then close the middle drawer of the cabinet. | `anlgx_170__close_the_middle_drawer_of_the_wooden_cabinet` | cheese_bowl=original LIBERO-Goal; close_middle=5/5 |
| `VCN14A_007` | `VCN14A_009` | `plate_placement_then_drawer_close` | Put the black bowl on the plate, then close the bottom drawer of the cabinet. | `anlgx_171__close_the_bottom_drawer_of_the_wooden_cabinet` | bowl_plate=original LIBERO-Goal; close_bottom=1/5 |
| `VCN14A_008` | `VCN14A_010` | `stove_placement_then_drawer_close` | Put the black bowl on the stove, then close the middle drawer of the cabinet. | `anlgx_170__close_the_middle_drawer_of_the_wooden_cabinet` | bowl_stove=original LIBERO-Goal; close_middle=5/5 |
| `VCN14A_009` | `VCN14A_011` | `cabinet_placement_then_drawer_close` | Put the black bowl on top of the cabinet, then close the top drawer of the cabinet. | `anlgx_169__close_the_top_drawer_of_the_wooden_cabinet` | bowl_cabinet=original LIBERO-Goal; close_top=3/5 |
| `VCN14A_010` | `VCN14A_012` | `plate_placement_then_stove_control` | Put the cream cheese on the plate, then turn on the stove. | `anlgx_141__put_the_cream_cheese_on_the_plate` | cheese_plate=1/5; turn_on=original LIBERO-Goal |
| `VCN14A_011` | `VCN14A_013` | `rack_placement_then_stove_control` | Put the black bowl on the wine rack, then turn on the stove. | `anlgx_129__put_the_black_bowl_on_the_wine_rack` | bowl_rack=1/5; turn_on=original LIBERO-Goal |
| `VCN14A_012` | `VCN14A_014` | `cabinet_placement_then_stove_control` | Put the plate on the top of the wooden cabinet, then turn on the stove. | `anlgx_134__put_the_plate_on_the_top_of_the_wooden_cabinet` | plate_cabinet=1/5; turn_on=original LIBERO-Goal |

## Excluded by the original physical screen

Source: `LIBERO_EX_ICRA27/LiberoValidComposeNew20260905/BATCH14A_PHYSICAL_SCREEN.json` (`774e113ee1fd7820ae5af2a40f091170707c59dc92d37a1055e5c1351a4f2701`).

| Original ID | Instruction | Physical exclusion |
|---|---|---|
| `VCN14A_002` | Put the chocolate pudding on the black bowl, then open the bottom drawer of the cabinet. | All five states failed the bottom-drawer full articulation sweep: plate_1 penetrated wooden_cabinet_1 by approximately 0.00050–0.00345 m. Initial goals, masks, and replay otherwise passed. |
| `VCN14A_006` | Put the cream cheese on the plate, then open the bottom drawer of the cabinet. | All five states failed the bottom-drawer full articulation sweep: plate_1 penetrated wooden_cabinet_1 by approximately 0.00056–0.00345 m. Initial goals, masks, and replay otherwise passed. |
| `VCN14A_015` | Put the white mug in the microwave, then close the microwave. | States 0, 2, and 4 failed the microwave-close full articulation sweep: porcelain_mug_1 penetrated microwave_1 by approximately 0.00127–0.00527 m; only states 1 and 3 passed all physical gates. |

## Validation


- Each task uses one already evaluated atomic donor BDDL as its complete scene and copies exactly five donor states byte-for-byte. No fixture, object, region, or pose is synthesized or removed.
- Every instruction contains exactly two action-only clauses: placement/containment first, control second.
- Success is two strict ordered native events plus both final BDDL predicates. Compose final completion has no TC threshold.
- Retained drawer masks select only the requested moving drawer part, and retained stove control selects only `flat_stove_1_button`.
- The action added to the exact donor has a numeric source-pose proof in `SOURCE_COMPATIBILITY.json`.
- Every final predicate must be false after the evaluator-identical ten wait steps in all five states.
- Native articulation dead-bands are valid initial states: the builder never additionally requires `Close`, `Open`, `Turnoff`, or another opposite endpoint predicate.
- Every state must have empty initial and settled cross-entity penetration, every exact mask at least 10 pixels at 320×320, and deterministic replay within 1e-8 m.
- Every requested control passes a full current-to-native-endpoint articulation sweep with no cross-entity penetration and a true native endpoint predicate.
- Ordered sequence, unordered final-goal set, and semantic-alias final-goal set must be absent from LIBERO-40, selected Compose, every workspace `TASK_INDEX.tsv`, every workspace BDDL, every instrumented result, explicit VCN11–13 source definitions, and this batch's other candidates. Coverage of VCN1–13 is asserted.
- The immutable original 15-candidate physical-screen report is audited before build. Its 12 valid original IDs are mapped to contiguous retained IDs; all three physical exclusions and their measured collision reasons are preserved in selection manifests.
- Gripper trajectory is a soft empirical prior, not a hard exclusion rule.

