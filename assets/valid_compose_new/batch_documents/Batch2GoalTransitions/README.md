# LIBERO Composition — 439 candidate screen

- Candidates: **12**
- Planned evaluation: **60 episodes** (5/task)
- Status: definitions, fixed init states, source comparison PNGs, and exact-mask validation complete; policy inference not run yet
- Rules: [COMPOSITION_RULES.md](COMPOSITION_RULES.md)

## Family counts

| Family | Tasks |
|---|---:|
| `goal_transition_permutation` | 12 |

## Candidate inventory

| ID | Steps | Pure | Instruction | Final goals | Compare |
|---|---:|---|---|---|---|
| `VCN2_001` | 2 | `true` | Open the middle drawer of the wooden cabinet, then put the cream cheese on the black bowl. | `open(wooden_cabinet_1_middle_region); on(cream_cheese_1, akita_black_bowl_1)` | [PNG](comparison_png/VCN2_001__scene.png) |
| `VCN2_002` | 2 | `true` | Turn on the stove, then put the cream cheese on the black bowl. | `turnon(flat_stove_1); on(cream_cheese_1, akita_black_bowl_1)` | [PNG](comparison_png/VCN2_002__masked_scene.png) |
| `VCN2_003` | 2 | `true` | Push the plate to the front of the stove, then put the cream cheese on the black bowl. | `on(plate_1, main_table_stove_front_region); on(cream_cheese_1, akita_black_bowl_1)` | [PNG](comparison_png/VCN2_003__masked_scene.png) |
| `VCN2_004` | 2 | `true` | Open the middle drawer of the wooden cabinet, then push the plate to the front of the stove. | `open(wooden_cabinet_1_middle_region); on(plate_1, main_table_stove_front_region)` | [PNG](comparison_png/VCN2_004__comparison.png) |
| `VCN2_005` | 2 | `true` | Turn on the stove, then push the plate to the front of the stove. | `turnon(flat_stove_1); on(plate_1, main_table_stove_front_region)` | [PNG](comparison_png/VCN2_005__comparison.png) |
| `VCN2_006` | 3 | `true` | Open the middle drawer of the wooden cabinet, then put the cream cheese on the black bowl, and finally turn on the stove. | `open(wooden_cabinet_1_middle_region); on(cream_cheese_1, akita_black_bowl_1); turnon(flat_stove_1)` | [PNG](comparison_png/VCN2_006__comparison.png) |
| `VCN2_007` | 3 | `true` | Turn on the stove, then put the cream cheese on the black bowl, and finally open the middle drawer of the wooden cabinet. | `turnon(flat_stove_1); on(cream_cheese_1, akita_black_bowl_1); open(wooden_cabinet_1_middle_region)` | [PNG](comparison_png/VCN2_007__masked_scene.png) |
| `VCN2_008` | 3 | `true` | Push the plate to the front of the stove, then put the cream cheese on the black bowl, and finally turn on the stove. | `on(plate_1, main_table_stove_front_region); on(cream_cheese_1, akita_black_bowl_1); turnon(flat_stove_1)` | [PNG](comparison_png/VCN2_008__masked_scene.png) |
| `VCN2_009` | 3 | `true` | Turn on the stove, then push the plate to the front of the stove, and finally open the middle drawer of the wooden cabinet. | `turnon(flat_stove_1); on(plate_1, main_table_stove_front_region); open(wooden_cabinet_1_middle_region)` | [PNG](comparison_png/VCN2_009__masked_scene.png) |
| `VCN2_010` | 3 | `true` | Open the middle drawer of the wooden cabinet, then turn on the stove, and finally put the cream cheese on the black bowl. | `open(wooden_cabinet_1_middle_region); turnon(flat_stove_1); on(cream_cheese_1, akita_black_bowl_1)` | [PNG](comparison_png/VCN2_010__comparison.png) |
| `VCN2_011` | 3 | `true` | Turn on the stove, then open the middle drawer of the wooden cabinet, and finally put the cream cheese on the black bowl. | `turnon(flat_stove_1); open(wooden_cabinet_1_middle_region); on(cream_cheese_1, akita_black_bowl_1)` | [PNG](comparison_png/VCN2_011__scene.png) |
| `VCN2_012` | 3 | `true` | Push the plate to the front of the stove, then open the middle drawer of the wooden cabinet, and finally put the cream cheese on the black bowl. | `on(plate_1, main_table_stove_front_region); open(wooden_cabinet_1_middle_region); on(cream_cheese_1, akita_black_bowl_1)` | [PNG](comparison_png/VCN2_012__masked_scene.png) |
