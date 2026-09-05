        # LIBERO Compose 350 candidate rules

        Identity is `physical scene + frozenset(final goal atoms)`. Rewordings and
        action-order permutations are not new tasks. Existing LIBERO-40,
        LiberoComposition-439, and LiberoComposition2Step-361 identities are excluded.

        - Object: enumerate every C(6,4) subset in all ten original layouts.
        - LIBERO-10 baskets: add the Scene1 C(4,4) task; remove the documented milk
          blocker from Scene2 and enumerate every C(6,3) and C(6,4) subset.
        - Goal: enumerate all 67 four-cliques of the audited 37-edge compatibility graph.
        - Goal+basket: add one basket at the robot-left donor pose, then compose cream
          cheese -> basket with every compatible one-, two-, and three-Goal clique that
          does not assign cream cheese to another destination.
        - Hybrids: explicitly test ordered open/insert/close, two opposed stoves, two
          cabinets plus rack, Scene5+Scene6 plate/pudding, and Scene8 with stove-off init.

        Temporal tasks carry `sequence_stages`; ordinary tasks use final conjunction.
        Stove turns expose only the exact requested knob instance. Every table region is
        projected from the current BDDL, and repeated objects/fixtures are never unioned.

        | Family | Tasks |
        |---|---:|
        | `X1_object_layout_four_to_basket` | 150 |
| `X2_libero10_scene1_four_to_basket` | 1 |
| `X3_libero10_scene2_milk_removed_3_to_basket` | 20 |
| `X4_libero10_scene2_milk_removed_4_to_basket` | 15 |
| `X5_goal_four_task_clique` | 67 |
| `X6_goal_plus_left_basket_2_task` | 9 |
| `X7_goal_plus_left_basket_3_task` | 28 |
| `X8_goal_plus_left_basket_4_task` | 40 |
| `X9_goal_open_insert_close_sequence` | 2 |
| `X10_kitchen3_two_stove_temporal_transfer` | 2 |
| `X11_kitchen4_goal_two_cabinet_hybrid` | 11 |
| `X12_living5_plus_scene6_pudding_plate_hybrid` | 4 |
| `X13_kitchen8_two_moka_then_turn_on` | 1 |

        **Total: 350 tasks / 1750 episodes.**
