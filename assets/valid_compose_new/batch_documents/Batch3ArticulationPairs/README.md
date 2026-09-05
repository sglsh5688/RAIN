# LIBERO Composition — 439 candidate screen

- Candidates: **6**
- Planned evaluation: **30 episodes** (5/task)
- Status: definitions, fixed init states, source comparison PNGs, and exact-mask validation complete; policy inference not run yet
- Rules: [COMPOSITION_RULES.md](COMPOSITION_RULES.md)

## Family counts

| Family | Tasks |
|---|---:|
| `paired_articulation_order` | 6 |

## Candidate inventory

| ID | Steps | Pure | Instruction | Final goals | Compare |
|---|---:|---|---|---|---|
| `VCN3_001` | 2 | `true` | Close the top drawer of the white cabinet, then close the bottom drawer of the white cabinet. | `close(white_cabinet_1_top_region); close(white_cabinet_1_bottom_region)` | [PNG](comparison_png/VCN3_001__comparison.png) |
| `VCN3_002` | 2 | `true` | Close the bottom drawer of the white cabinet, then close the top drawer of the white cabinet. | `close(white_cabinet_1_bottom_region); close(white_cabinet_1_top_region)` | [PNG](comparison_png/VCN3_002__comparison.png) |
| `VCN3_003` | 2 | `true` | Close the middle drawer of the white cabinet, then close the bottom drawer of the white cabinet. | `close(white_cabinet_1_middle_region); close(white_cabinet_1_bottom_region)` | [PNG](comparison_png/VCN3_003__scene.png) |
| `VCN3_004` | 2 | `true` | Close the bottom drawer of the white cabinet, then close the middle drawer of the white cabinet. | `close(white_cabinet_1_bottom_region); close(white_cabinet_1_middle_region)` | [PNG](comparison_png/VCN3_004__scene.png) |
| `VCN3_005` | 2 | `true` | Close the bottom drawer of the white cabinet, then close the microwave door. | `close(white_cabinet_1_bottom_region); close(microwave_1)` | [PNG](comparison_png/VCN3_005__comparison.png) |
| `VCN3_006` | 2 | `true` | Close the microwave door, then close the bottom drawer of the white cabinet. | `close(microwave_1); close(white_cabinet_1_bottom_region)` | [PNG](comparison_png/VCN3_006__masked_scene.png) |
