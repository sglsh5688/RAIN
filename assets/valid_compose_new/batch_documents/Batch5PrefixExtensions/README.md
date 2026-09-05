# LIBERO Composition — 439 candidate screen

- Candidates: **8**
- Planned evaluation: **40 episodes** (5/task)
- Status: definitions, fixed init states, source comparison PNGs, and exact-mask validation complete; policy inference not run yet
- Rules: [COMPOSITION_RULES.md](COMPOSITION_RULES.md)

## Family counts

| Family | Tasks |
|---|---:|
| `long04_prefix_then_top_close` | 1 |
| `long04_prefix_then_middle_close` | 1 |
| `mkdc_prefix_then_top_close` | 1 |
| `mkdc_prefix_then_middle_close` | 1 |
| `reverse_mkdc_control` | 1 |
| `microwave_first_then_long04` | 1 |
| `successful_goal_prefix_then_stove` | 1 |
| `successful_goal_prefix_then_push` | 1 |

## Candidate inventory

| ID | Steps | Pure | Instruction | Final goals | Compare |
|---|---:|---|---|---|---|
| `VCN5_001` | 3 | `true` | Put the black bowl in the bottom drawer of the white cabinet, then close the bottom drawer of the white cabinet, and finally close the top drawer of the white cabinet. | `in(akita_black_bowl_1, white_cabinet_1_bottom_region); close(white_cabinet_1_bottom_region); close(white_cabinet_1_top_region)` | [PNG](comparison_png/VCN5_001__comparison.png) |
| `VCN5_002` | 3 | `true` | Put the black bowl in the bottom drawer of the white cabinet, then close the bottom drawer of the white cabinet, and finally close the middle drawer of the white cabinet. | `in(akita_black_bowl_1, white_cabinet_1_bottom_region); close(white_cabinet_1_bottom_region); close(white_cabinet_1_middle_region)` | [PNG](comparison_png/VCN5_002__comparison.png) |
| `VCN5_003` | 3 | `true` | Put the moka pot on the stove, then close the bottom drawer of the white cabinet, and finally close the top drawer of the white cabinet. | `on(moka_pot_2, flat_stove_1_cook_region); close(white_cabinet_1_bottom_region); close(white_cabinet_1_top_region)` | [PNG](comparison_png/VCN5_003__scene.png) |
| `VCN5_004` | 3 | `true` | Put the moka pot on the stove, then close the bottom drawer of the white cabinet, and finally close the middle drawer of the white cabinet. | `on(moka_pot_2, flat_stove_1_cook_region); close(white_cabinet_1_bottom_region); close(white_cabinet_1_middle_region)` | [PNG](comparison_png/VCN5_004__comparison.png) |
| `VCN5_005` | 2 | `true` | Close the bottom drawer of the white cabinet, then put the moka pot on the stove. | `close(white_cabinet_1_bottom_region); on(moka_pot_2, flat_stove_1_cook_region)` | [PNG](comparison_png/VCN5_005__scene.png) |
| `VCN5_006` | 3 | `true` | Close the microwave door, then put the black bowl in the bottom drawer of the white cabinet, and finally close the bottom drawer of the white cabinet. | `close(microwave_1); in(akita_black_bowl_1, white_cabinet_1_bottom_region); close(white_cabinet_1_bottom_region)` | [PNG](comparison_png/VCN5_006__scene.png) |
| `VCN5_007` | 3 | `true` | Put the cream cheese on the black bowl, then open the middle drawer of the wooden cabinet, and finally turn on the stove. | `on(cream_cheese_1, akita_black_bowl_1); open(wooden_cabinet_1_middle_region); turnon(flat_stove_1)` | [PNG](comparison_png/VCN5_007__comparison.png) |
| `VCN5_008` | 3 | `true` | Put the cream cheese on the black bowl, then open the middle drawer of the wooden cabinet, and finally push the plate to the front of the stove. | `on(cream_cheese_1, akita_black_bowl_1); open(wooden_cabinet_1_middle_region); on(plate_1, main_table_stove_front_region)` | [PNG](comparison_png/VCN5_008__scene.png) |
