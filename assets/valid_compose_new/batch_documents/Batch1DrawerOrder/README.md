# LIBERO Composition — 439 candidate screen

- Candidates: **14**
- Planned evaluation: **70 episodes** (5/task)
- Status: definitions, fixed init states, source comparison PNGs, and exact-mask validation complete; policy inference not run yet
- Rules: [COMPOSITION_RULES.md](COMPOSITION_RULES.md)

## Family counts

| Family | Tasks |
|---|---:|
| `upper_close_then_original_bowl_close` | 2 |
| `upper_close_then_bowl_insert` | 2 |
| `bowl_insert_then_upper_close` | 2 |
| `drawer_close_then_moka` | 2 |
| `moka_then_upper_drawer_close` | 2 |
| `upper_close_moka_bottom_close` | 2 |
| `moka_two_drawer_close` | 2 |

## Candidate inventory

| ID | Steps | Pure | Instruction | Final goals | Compare |
|---|---:|---|---|---|---|
| `VCN1_001` | 3 | `true` | Close the top drawer of the white cabinet, then put the black bowl in the bottom drawer of the white cabinet, and finally close the bottom drawer of the white cabinet. | `close(white_cabinet_1_top_region); in(akita_black_bowl_1, white_cabinet_1_bottom_region); close(white_cabinet_1_bottom_region)` | [PNG](comparison_png/VCN1_001__masked_scene.png) |
| `VCN1_002` | 3 | `true` | Close the middle drawer of the white cabinet, then put the black bowl in the bottom drawer of the white cabinet, and finally close the bottom drawer of the white cabinet. | `close(white_cabinet_1_middle_region); in(akita_black_bowl_1, white_cabinet_1_bottom_region); close(white_cabinet_1_bottom_region)` | [PNG](comparison_png/VCN1_002__comparison.png) |
| `VCN1_003` | 2 | `true` | Close the top drawer of the white cabinet, then put the black bowl in the bottom drawer of the white cabinet. | `close(white_cabinet_1_top_region); in(akita_black_bowl_1, white_cabinet_1_bottom_region)` | [PNG](comparison_png/VCN1_003__scene.png) |
| `VCN1_004` | 2 | `true` | Close the middle drawer of the white cabinet, then put the black bowl in the bottom drawer of the white cabinet. | `close(white_cabinet_1_middle_region); in(akita_black_bowl_1, white_cabinet_1_bottom_region)` | [PNG](comparison_png/VCN1_004__scene.png) |
| `VCN1_005` | 2 | `true` | Put the black bowl in the bottom drawer of the white cabinet, then close the top drawer of the white cabinet. | `in(akita_black_bowl_1, white_cabinet_1_bottom_region); close(white_cabinet_1_top_region)` | [PNG](comparison_png/VCN1_005__comparison.png) |
| `VCN1_006` | 2 | `true` | Put the black bowl in the bottom drawer of the white cabinet, then close the middle drawer of the white cabinet. | `in(akita_black_bowl_1, white_cabinet_1_bottom_region); close(white_cabinet_1_middle_region)` | [PNG](comparison_png/VCN1_006__masked_scene.png) |
| `VCN1_007` | 2 | `true` | Close the top drawer of the white cabinet, then put the moka pot on the stove. | `close(white_cabinet_1_top_region); on(moka_pot_2, flat_stove_1_cook_region)` | [PNG](comparison_png/VCN1_007__scene.png) |
| `VCN1_008` | 2 | `true` | Close the middle drawer of the white cabinet, then put the moka pot on the stove. | `close(white_cabinet_1_middle_region); on(moka_pot_2, flat_stove_1_cook_region)` | [PNG](comparison_png/VCN1_008__masked_scene.png) |
| `VCN1_009` | 2 | `true` | Put the moka pot on the stove, then close the top drawer of the white cabinet. | `on(moka_pot_2, flat_stove_1_cook_region); close(white_cabinet_1_top_region)` | [PNG](comparison_png/VCN1_009__masked_scene.png) |
| `VCN1_010` | 2 | `true` | Put the moka pot on the stove, then close the middle drawer of the white cabinet. | `on(moka_pot_2, flat_stove_1_cook_region); close(white_cabinet_1_middle_region)` | [PNG](comparison_png/VCN1_010__comparison.png) |
| `VCN1_011` | 3 | `true` | Close the top drawer of the white cabinet, then put the moka pot on the stove, and finally close the bottom drawer of the white cabinet. | `close(white_cabinet_1_top_region); on(moka_pot_2, flat_stove_1_cook_region); close(white_cabinet_1_bottom_region)` | [PNG](comparison_png/VCN1_011__masked_scene.png) |
| `VCN1_012` | 3 | `true` | Close the middle drawer of the white cabinet, then put the moka pot on the stove, and finally close the bottom drawer of the white cabinet. | `close(white_cabinet_1_middle_region); on(moka_pot_2, flat_stove_1_cook_region); close(white_cabinet_1_bottom_region)` | [PNG](comparison_png/VCN1_012__scene.png) |
| `VCN1_013` | 3 | `true` | Put the moka pot on the stove, then close the top drawer of the white cabinet, and finally close the bottom drawer of the white cabinet. | `on(moka_pot_2, flat_stove_1_cook_region); close(white_cabinet_1_top_region); close(white_cabinet_1_bottom_region)` | [PNG](comparison_png/VCN1_013__comparison.png) |
| `VCN1_014` | 3 | `true` | Put the moka pot on the stove, then close the middle drawer of the white cabinet, and finally close the bottom drawer of the white cabinet. | `on(moka_pot_2, flat_stove_1_cook_region); close(white_cabinet_1_middle_region); close(white_cabinet_1_bottom_region)` | [PNG](comparison_png/VCN1_014__comparison.png) |
