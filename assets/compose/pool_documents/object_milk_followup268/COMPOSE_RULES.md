# Compose Object/milk follow-up rules

This is an intervention screen, not a repetition of the unchanged Object combinatorial baseline.

## Existing controls (already evaluated, five episodes per task)

| Control | Tasks | Episodes | Successful tasks |
|---|---:|---:|---:|
| Stock Object layouts, all 3-object subsets (`C11`) | 200 | 1,000 | 0 |
| Stock Object layouts, all 4-object subsets (`X1`) | 150 | 750 | 0 |
| Stock LIBERO-10 Scene 2 `COMP_209` | 1 | 5 | 1 (1/5 episodes) |
| Milk-removed LIBERO-10 `COMPOSE_155` | 1 | 5 | 1 (2/5 episodes) |
| Milk-removed COMPOSE_155 four-object supersets (`174/176/177`) | 3 | 15 | 0 |

## New interventions

- `milk_first_temporal`: stock layout, but cumulative temporal stages require milk to be placed first.
- `milk_beside_ketchup`: Scene 2 milk is moved beside ketchup and new stable states are generated.
- `milk_upper_slot_swap`: in five Object scenes, milk swaps with the object in the upper/back slot.
- `compose155_prefix_append`: reuse exact COMPOSE_155 states, complete its three successful-prefix objects, then append one fourth object.
- Tasks without a sequence intervention retain ordinary conjunction scoring; their explicit action plan supplies a deterministic order.

| Family | Tasks |
|---|---:|
| `L1_long_milk_first_3_to_basket` | 15 |
| `L1_long_milk_first_4_to_basket` | 20 |
| `L2_long_milk_beside_ketchup_3_to_basket` | 20 |
| `L2_long_milk_beside_ketchup_4_to_basket` | 15 |
| `L3_compose155_prefix_then_append_fourth` | 3 |
| `O1_object_milk_first_3_to_basket` | 60 |
| `O1_object_milk_first_4_to_basket` | 60 |
| `O2_object_milk_upper_swap_3_to_basket` | 50 |
| `O2_object_milk_upper_swap_4_to_basket` | 25 |

Total: **268 tasks / 1340 episodes**; 158 tasks use temporal stage scoring.
