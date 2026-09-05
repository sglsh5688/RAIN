# LIBERO Composition — 439 candidate screen

- Candidates: **12**
- Planned evaluation: **60 episodes** (5/task)
- Status: definitions, fixed init states, source comparison PNGs, and exact-mask validation complete; policy inference not run yet
- Rules: [COMPOSITION_RULES.md](COMPOSITION_RULES.md)

## Family counts

| Family | Tasks |
|---|---:|
| `middle_insert_then_same_drawer_close` | 1 |
| `upper_close_then_middle_insert` | 1 |
| `middle_insert_then_upper_close` | 1 |
| `upper_close_then_middle_insert_close` | 1 |
| `middle_insert_close_then_upper_close` | 1 |
| `bottom_close_then_middle_insert` | 1 |
| `middle_insert_then_bottom_close` | 1 |
| `bottom_close_then_middle_insert_close` | 1 |
| `middle_insert_close_then_bottom_close` | 1 |
| `middle_insert_then_two_closes` | 1 |
| `upper_close_middle_insert_bottom_close` | 1 |
| `middle_insert_then_bottom_upper_close` | 1 |

## Candidate inventory

| ID | Steps | Pure | Instruction | Final goals | Compare |
|---|---:|---|---|---|---|
| `VCN4_001` | 2 | `true` | Put the black bowl in the middle drawer of the white cabinet, then close the middle drawer of the white cabinet. | `in(akita_black_bowl_1, white_cabinet_1_middle_region); close(white_cabinet_1_middle_region)` | [PNG](comparison_png/VCN4_001__comparison.png) |
| `VCN4_002` | 2 | `true` | Close the top drawer of the white cabinet, then put the black bowl in the middle drawer of the white cabinet. | `close(white_cabinet_1_top_region); in(akita_black_bowl_1, white_cabinet_1_middle_region)` | [PNG](comparison_png/VCN4_002__scene.png) |
| `VCN4_003` | 2 | `true` | Put the black bowl in the middle drawer of the white cabinet, then close the top drawer of the white cabinet. | `in(akita_black_bowl_1, white_cabinet_1_middle_region); close(white_cabinet_1_top_region)` | [PNG](comparison_png/VCN4_003__masked_scene.png) |
| `VCN4_004` | 3 | `true` | Close the top drawer of the white cabinet, then put the black bowl in the middle drawer of the white cabinet, and finally close the middle drawer of the white cabinet. | `close(white_cabinet_1_top_region); in(akita_black_bowl_1, white_cabinet_1_middle_region); close(white_cabinet_1_middle_region)` | [PNG](comparison_png/VCN4_004__masked_scene.png) |
| `VCN4_005` | 3 | `true` | Put the black bowl in the middle drawer of the white cabinet, then close the middle drawer of the white cabinet, and finally close the top drawer of the white cabinet. | `in(akita_black_bowl_1, white_cabinet_1_middle_region); close(white_cabinet_1_middle_region); close(white_cabinet_1_top_region)` | [PNG](comparison_png/VCN4_005__masked_scene.png) |
| `VCN4_006` | 2 | `true` | Close the bottom drawer of the white cabinet, then put the black bowl in the middle drawer of the white cabinet. | `close(white_cabinet_1_bottom_region); in(akita_black_bowl_1, white_cabinet_1_middle_region)` | [PNG](comparison_png/VCN4_006__scene.png) |
| `VCN4_007` | 2 | `true` | Put the black bowl in the middle drawer of the white cabinet, then close the bottom drawer of the white cabinet. | `in(akita_black_bowl_1, white_cabinet_1_middle_region); close(white_cabinet_1_bottom_region)` | [PNG](comparison_png/VCN4_007__masked_scene.png) |
| `VCN4_008` | 3 | `true` | Close the bottom drawer of the white cabinet, then put the black bowl in the middle drawer of the white cabinet, and finally close the middle drawer of the white cabinet. | `close(white_cabinet_1_bottom_region); in(akita_black_bowl_1, white_cabinet_1_middle_region); close(white_cabinet_1_middle_region)` | [PNG](comparison_png/VCN4_008__comparison.png) |
| `VCN4_009` | 3 | `true` | Put the black bowl in the middle drawer of the white cabinet, then close the middle drawer of the white cabinet, and finally close the bottom drawer of the white cabinet. | `in(akita_black_bowl_1, white_cabinet_1_middle_region); close(white_cabinet_1_middle_region); close(white_cabinet_1_bottom_region)` | [PNG](comparison_png/VCN4_009__comparison.png) |
| `VCN4_010` | 3 | `true` | Put the black bowl in the middle drawer of the white cabinet, then close the top drawer of the white cabinet, and finally close the middle drawer of the white cabinet. | `in(akita_black_bowl_1, white_cabinet_1_middle_region); close(white_cabinet_1_top_region); close(white_cabinet_1_middle_region)` | [PNG](comparison_png/VCN4_010__scene.png) |
| `VCN4_011` | 3 | `true` | Close the top drawer of the white cabinet, then put the black bowl in the middle drawer of the white cabinet, and finally close the bottom drawer of the white cabinet. | `close(white_cabinet_1_top_region); in(akita_black_bowl_1, white_cabinet_1_middle_region); close(white_cabinet_1_bottom_region)` | [PNG](comparison_png/VCN4_011__masked_scene.png) |
| `VCN4_012` | 3 | `true` | Put the black bowl in the middle drawer of the white cabinet, then close the bottom drawer of the white cabinet, and finally close the top drawer of the white cabinet. | `in(akita_black_bowl_1, white_cabinet_1_middle_region); close(white_cabinet_1_bottom_region); close(white_cabinet_1_top_region)` | [PNG](comparison_png/VCN4_012__comparison.png) |
