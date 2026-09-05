# LIBERO Composition — 439 candidate screen

- Candidates: **7**
- Planned evaluation: **35 episodes** (5/task)
- Status: definitions, fixed init states, source comparison PNGs, and exact-mask validation complete; policy inference not run yet
- Rules: [COMPOSITION_RULES.md](COMPOSITION_RULES.md)

## Family counts

| Family | Tasks |
|---|---:|
| `successful_bowl_middle_close_prefix_then_bottom` | 1 |
| `upper_drawer_pair` | 1 |
| `upper_drawer_reverse_pair` | 1 |
| `top_middle_bottom_order` | 1 |
| `middle_top_bottom_order` | 1 |
| `successful_top_bottom_prefix_extension` | 1 |
| `successful_middle_bottom_prefix_extension` | 1 |

## Candidate inventory

| ID | Steps | Pure | Instruction | Final goals | Compare |
|---|---:|---|---|---|---|
| `VCN6_001` | 3 | `true` | Put the black bowl in the bottom drawer of the white cabinet, then close the middle drawer of the white cabinet, and finally close the bottom drawer of the white cabinet. | `in(akita_black_bowl_1, white_cabinet_1_bottom_region); close(white_cabinet_1_middle_region); close(white_cabinet_1_bottom_region)` | [PNG](comparison_png/VCN6_001__comparison.png) |
| `VCN6_002` | 2 | `true` | Close the top drawer of the white cabinet, then close the middle drawer of the white cabinet. | `close(white_cabinet_1_top_region); close(white_cabinet_1_middle_region)` | [PNG](comparison_png/VCN6_002__comparison.png) |
| `VCN6_003` | 2 | `true` | Close the middle drawer of the white cabinet, then close the top drawer of the white cabinet. | `close(white_cabinet_1_middle_region); close(white_cabinet_1_top_region)` | [PNG](comparison_png/VCN6_003__masked_scene.png) |
| `VCN6_004` | 3 | `true` | Close the top drawer of the white cabinet, then close the middle drawer of the white cabinet, and finally close the bottom drawer of the white cabinet. | `close(white_cabinet_1_top_region); close(white_cabinet_1_middle_region); close(white_cabinet_1_bottom_region)` | [PNG](comparison_png/VCN6_004__masked_scene.png) |
| `VCN6_005` | 3 | `true` | Close the middle drawer of the white cabinet, then close the top drawer of the white cabinet, and finally close the bottom drawer of the white cabinet. | `close(white_cabinet_1_middle_region); close(white_cabinet_1_top_region); close(white_cabinet_1_bottom_region)` | [PNG](comparison_png/VCN6_005__masked_scene.png) |
| `VCN6_006` | 3 | `true` | Close the top drawer of the white cabinet, then close the bottom drawer of the white cabinet, and finally close the middle drawer of the white cabinet. | `close(white_cabinet_1_top_region); close(white_cabinet_1_bottom_region); close(white_cabinet_1_middle_region)` | [PNG](comparison_png/VCN6_006__scene.png) |
| `VCN6_007` | 3 | `true` | Close the middle drawer of the white cabinet, then close the bottom drawer of the white cabinet, and finally close the top drawer of the white cabinet. | `close(white_cabinet_1_middle_region); close(white_cabinet_1_bottom_region); close(white_cabinet_1_top_region)` | [PNG](comparison_png/VCN6_007__masked_scene.png) |
