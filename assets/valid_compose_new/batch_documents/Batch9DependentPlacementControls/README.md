# LIBERO Composition — 439 candidate screen

- Candidates: **12**
- Planned evaluation: **60 episodes** (5/task)
- Status: definitions, fixed init states, source comparison PNGs, and exact-mask validation complete; policy inference not run yet
- Rules: [COMPOSITION_RULES.md](COMPOSITION_RULES.md)

## Family counts

| Family | Tasks |
|---|---:|
| `same_drawer_insert_then_close` | 3 |
| `insertion_then_sibling_open` | 1 |
| `drawer_then_knob_control` | 1 |
| `knob_control_then_cabinet_placement` | 1 |
| `cabinet_placement_then_control` | 1 |
| `stove_placement_then_drawer_control` | 2 |
| `stove_placement_then_knob_control` | 2 |
| `plate_placement_then_control` | 1 |

## Candidate inventory

| ID | Steps | Pure | Instruction | Final goals | Compare |
|---|---:|---|---|---|---|
| `VCN9_001` | 2 | `true` | Put the cream cheese in the top drawer of the wooden cabinet, then close the top drawer of the wooden cabinet. | `in(cream_cheese_1, wooden_cabinet_1_top_region); close(wooden_cabinet_1_top_region)` | [PNG](comparison_png/VCN9_001__scene.png) |
| `VCN9_002` | 2 | `true` | Put the cream cheese in the middle drawer of the wooden cabinet, then close the middle drawer of the wooden cabinet. | `in(cream_cheese_1, wooden_cabinet_1_middle_region); close(wooden_cabinet_1_middle_region)` | [PNG](comparison_png/VCN9_002__scene.png) |
| `VCN9_003` | 2 | `true` | Put the butter in the middle drawer of the wooden cabinet, then close the middle drawer of the wooden cabinet. | `in(butter_1, wooden_cabinet_1_middle_region); close(wooden_cabinet_1_middle_region)` | [PNG](comparison_png/VCN9_003__comparison.png) |
| `VCN9_004` | 2 | `true` | Put the cream cheese in the top drawer of the wooden cabinet, then open the middle drawer of the cabinet. | `in(cream_cheese_1, wooden_cabinet_1_top_region); open(wooden_cabinet_1_middle_region)` | [PNG](comparison_png/VCN9_004__comparison.png) |
| `VCN9_005` | 2 | `true` | Close the middle drawer of the wooden cabinet, then turn on the stove. | `close(wooden_cabinet_1_middle_region); turnon(flat_stove_1)` | [PNG](comparison_png/VCN9_005__comparison.png) |
| `VCN9_006` | 2 | `true` | Turn on the stove, then put the butter on the top of the wooden cabinet. | `turnon(flat_stove_1); on(butter_1, wooden_cabinet_1_top_side)` | [PNG](comparison_png/VCN9_006__scene.png) |
| `VCN9_007` | 2 | `true` | Put the butter on the top of the wooden cabinet, then close the middle drawer of the wooden cabinet. | `on(butter_1, wooden_cabinet_1_top_side); close(wooden_cabinet_1_middle_region)` | [PNG](comparison_png/VCN9_007__comparison.png) |
| `VCN9_008` | 2 | `true` | Put the cream cheese on the stove, then close the middle drawer of the wooden cabinet. | `on(cream_cheese_1, flat_stove_1_cook_region); close(wooden_cabinet_1_middle_region)` | [PNG](comparison_png/VCN9_008__scene.png) |
| `VCN9_009` | 2 | `true` | Put the chocolate pudding on the stove, then close the middle drawer of the wooden cabinet. | `on(chocolate_pudding_1, flat_stove_1_cook_region); close(wooden_cabinet_1_middle_region)` | [PNG](comparison_png/VCN9_009__comparison.png) |
| `VCN9_010` | 2 | `true` | Put the cream cheese on the stove, then turn on the stove. | `on(cream_cheese_1, flat_stove_1_cook_region); turnon(flat_stove_1)` | [PNG](comparison_png/VCN9_010__masked_scene.png) |
| `VCN9_011` | 2 | `true` | Put the chocolate pudding on the stove, then turn on the stove. | `on(chocolate_pudding_1, flat_stove_1_cook_region); turnon(flat_stove_1)` | [PNG](comparison_png/VCN9_011__masked_scene.png) |
| `VCN9_012` | 2 | `true` | Put the chocolate pudding on the plate, then close the middle drawer of the wooden cabinet. | `on(chocolate_pudding_1, plate_1); close(wooden_cabinet_1_middle_region)` | [PNG](comparison_png/VCN9_012__masked_scene.png) |
