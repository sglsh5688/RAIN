# LIBERO Composition — 439 candidate screen

- Candidates: **6**
- Planned evaluation: **30 episodes** (5/task)
- Status: definitions, fixed init states, source comparison PNGs, and exact-mask validation complete; policy inference not run yet
- Rules: [COMPOSITION_RULES.md](COMPOSITION_RULES.md)

## Family counts

| Family | Tasks |
|---|---:|
| `stove_placement_then_plate_push` | 2 |
| `plate_push_then_stove_placement` | 2 |
| `two_objects_distinct_caddy_compartments` | 1 |
| `two_objects_distinct_caddy_compartments_reverse` | 1 |

## Candidate inventory

| ID | Steps | Pure | Instruction | Final goals | Compare |
|---|---:|---|---|---|---|
| `VCN10_001` | 2 | `true` | Put the cream cheese on the stove, then push the plate to the front of the stove. | `on(cream_cheese_1, flat_stove_1_cook_region); on(plate_1, main_table_stove_front_region)` | [PNG](comparison_png/VCN10_001__scene.png) |
| `VCN10_002` | 2 | `true` | Push the plate to the front of the stove, then put the cream cheese on the stove. | `on(plate_1, main_table_stove_front_region); on(cream_cheese_1, flat_stove_1_cook_region)` | [PNG](comparison_png/VCN10_002__scene.png) |
| `VCN10_003` | 2 | `true` | Put the chocolate pudding on the stove, then push the plate to the front of the stove. | `on(chocolate_pudding_1, flat_stove_1_cook_region); on(plate_1, main_table_stove_front_region)` | [PNG](comparison_png/VCN10_003__comparison.png) |
| `VCN10_004` | 2 | `true` | Push the plate to the front of the stove, then put the chocolate pudding on the stove. | `on(plate_1, main_table_stove_front_region); on(chocolate_pudding_1, flat_stove_1_cook_region)` | [PNG](comparison_png/VCN10_004__scene.png) |
| `VCN10_005` | 2 | `true` | Put the salad dressing in the left compartment of the caddy, then put the yellow and white mug in the back compartment of the caddy. | `in(salad_dressing_1, desk_caddy_1_left_contain_region); in(white_yellow_mug_1, desk_caddy_1_back_contain_region)` | [PNG](comparison_png/VCN10_005__scene.png) |
| `VCN10_006` | 2 | `true` | Put the yellow and white mug in the back compartment of the caddy, then put the salad dressing in the left compartment of the caddy. | `in(white_yellow_mug_1, desk_caddy_1_back_contain_region); in(salad_dressing_1, desk_caddy_1_left_contain_region)` | [PNG](comparison_png/VCN10_006__scene.png) |
