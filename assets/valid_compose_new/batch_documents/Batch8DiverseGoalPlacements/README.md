# LIBERO Composition — 439 candidate screen

- Candidates: **12**
- Planned evaluation: **60 episodes** (5/task)
- Status: definitions, fixed init states, source comparison PNGs, and exact-mask validation complete; policy inference not run yet
- Rules: [COMPOSITION_RULES.md](COMPOSITION_RULES.md)

## Family counts

| Family | Tasks |
|---|---:|
| `control_then_stove_placement` | 2 |
| `control_then_cabinet_placement` | 2 |
| `control_then_container_placement` | 2 |
| `placement_then_open_transition` | 4 |
| `placement_then_control_soft_probe` | 2 |

## Candidate inventory

| ID | Steps | Pure | Instruction | Final goals | Compare |
|---|---:|---|---|---|---|
| `VCN8_001` | 2 | `true` | Close the middle drawer of the wooden cabinet, then put the chocolate pudding on the stove. | `close(wooden_cabinet_1_middle_region); on(chocolate_pudding_1, flat_stove_1_cook_region)` | [PNG](comparison_png/VCN8_001__masked_scene.png) |
| `VCN8_002` | 2 | `true` | Close the middle drawer of the wooden cabinet, then put the cream cheese on the stove. | `close(wooden_cabinet_1_middle_region); on(cream_cheese_1, flat_stove_1_cook_region)` | [PNG](comparison_png/VCN8_002__scene.png) |
| `VCN8_003` | 2 | `true` | Close the middle drawer of the wooden cabinet, then put the butter on the top of the wooden cabinet. | `close(wooden_cabinet_1_middle_region); on(butter_1, wooden_cabinet_1_top_side)` | [PNG](comparison_png/VCN8_003__scene.png) |
| `VCN8_004` | 2 | `true` | Close the top drawer of the wooden cabinet, then put the butter on the top of the wooden cabinet. | `close(wooden_cabinet_1_top_region); on(butter_1, wooden_cabinet_1_top_side)` | [PNG](comparison_png/VCN8_004__comparison.png) |
| `VCN8_005` | 2 | `true` | Close the middle drawer of the wooden cabinet, then put the butter on the black bowl. | `close(wooden_cabinet_1_middle_region); on(butter_1, akita_black_bowl_1)` | [PNG](comparison_png/VCN8_005__masked_scene.png) |
| `VCN8_006` | 2 | `true` | Close the top drawer of the wooden cabinet, then put the chocolate pudding on the black bowl. | `close(wooden_cabinet_1_top_region); on(chocolate_pudding_1, akita_black_bowl_1)` | [PNG](comparison_png/VCN8_006__scene.png) |
| `VCN8_007` | 2 | `true` | Put the butter on the black bowl, then open the middle drawer of the cabinet. | `on(butter_1, akita_black_bowl_1); open(wooden_cabinet_1_middle_region)` | [PNG](comparison_png/VCN8_007__masked_scene.png) |
| `VCN8_008` | 2 | `true` | Put the chocolate pudding on the black bowl, then open the middle drawer of the cabinet. | `on(chocolate_pudding_1, akita_black_bowl_1); open(wooden_cabinet_1_middle_region)` | [PNG](comparison_png/VCN8_008__comparison.png) |
| `VCN8_009` | 2 | `true` | Put the cream cheese on the stove, then open the middle drawer of the cabinet. | `on(cream_cheese_1, flat_stove_1_cook_region); open(wooden_cabinet_1_middle_region)` | [PNG](comparison_png/VCN8_009__masked_scene.png) |
| `VCN8_010` | 2 | `true` | Put the chocolate pudding on the stove, then open the middle drawer of the cabinet. | `on(chocolate_pudding_1, flat_stove_1_cook_region); open(wooden_cabinet_1_middle_region)` | [PNG](comparison_png/VCN8_010__masked_scene.png) |
| `VCN8_011` | 2 | `true` | Put the butter on the black bowl, then close the middle drawer of the wooden cabinet. | `on(butter_1, akita_black_bowl_1); close(wooden_cabinet_1_middle_region)` | [PNG](comparison_png/VCN8_011__masked_scene.png) |
| `VCN8_012` | 2 | `true` | Put the chocolate pudding on the black bowl, then close the middle drawer of the wooden cabinet. | `on(chocolate_pudding_1, akita_black_bowl_1); close(wooden_cabinet_1_middle_region)` | [PNG](comparison_png/VCN8_012__scene.png) |
