# LIBERO Composition — 439 candidate screen

- Candidates: **18**
- Planned evaluation: **90 episodes** (5/task)
- Status: definitions, fixed init states, source comparison PNGs, and exact-mask validation complete; policy inference not run yet
- Rules: [COMPOSITION_RULES.md](COMPOSITION_RULES.md)

## Family counts

| Family | Tasks |
|---|---:|
| `accepted_vcn10_prefix_then_drawer_open` | 2 |
| `accepted_vcn8_prefix_then_loaded_bowl_move` | 2 |
| `loaded_bowl_direct_move` | 1 |
| `lbcm_atomic_then_goal_drawer` | 1 |
| `accepted_vcn9_prefix_then_lbcm_atomic` | 1 |
| `ramekin_plate_then_stove_control` | 1 |
| `drawer_open_then_ramekin_plate` | 2 |
| `loaded_plate_push` | 1 |
| `loaded_plate_push_then_control` | 3 |
| `goal_with_source_aligned_basket` | 1 |
| `accepted_vcn9_prefix_then_ramekin_plate` | 1 |
| `accepted_vcn9_prefix_then_deliberate_close` | 1 |
| `ramekin_plate_then_drawer_open` | 1 |

## Candidate inventory

| ID | Steps | Pure | Instruction | Final goals | Compare |
|---|---:|---|---|---|---|
| `VCN19_001` | 3 | `true` | Put the cream cheese on the stove, then push the plate to the front of the stove, then open the middle drawer of the wooden cabinet. | `on(cream_cheese_1, flat_stove_1_cook_region); on(plate_1, main_table_stove_front_region); open(wooden_cabinet_1_middle_region)` | [PNG](comparison_png/VCN19_001__put_the_cream_cheese_on_the_stove_then_push_the_plate_to_the_front_of_the_stove_then_open_the_middle_drawer_of_the_wooden_cabinet.png) |
| `VCN19_002` | 3 | `true` | Put the cream cheese on the stove, then push the plate to the front of the stove, then open the bottom drawer of the wooden cabinet. | `on(cream_cheese_1, flat_stove_1_cook_region); on(plate_1, main_table_stove_front_region); open(wooden_cabinet_1_bottom_region)` | [PNG](comparison_png/VCN19_002__put_the_cream_cheese_on_the_stove_then_push_the_plate_to_the_front_of_the_stove_then_open_the_bottom_drawer_of_the_wooden_cabinet.png) |
| `VCN19_003` | 3 | `true` | Put the chocolate pudding on the black bowl, then open the middle drawer of the cabinet, then put the loaded black bowl in the middle drawer. | `on(chocolate_pudding_1, akita_black_bowl_1); open(wooden_cabinet_1_middle_region); in(akita_black_bowl_1, wooden_cabinet_1_middle_region)` | [PNG](comparison_png/VCN19_003__put_the_chocolate_pudding_on_the_black_bowl_then_open_the_middle_drawer_of_the_cabinet_then_put_the_loaded_black_bowl_in_the_middle_drawer.png) |
| `VCN19_004` | 2 | `true` | Put the chocolate pudding on the black bowl, then put the loaded black bowl on the plate. | `on(chocolate_pudding_1, akita_black_bowl_1); on(akita_black_bowl_1, plate_1)` | [PNG](comparison_png/VCN19_004__put_the_chocolate_pudding_on_the_black_bowl_then_put_the_loaded_black_bowl_on_the_plate.png) |
| `VCN19_005` | 2 | `true` | Put the tomato sauce in the basket, then open the middle drawer of the wooden cabinet. | `in(tomato_sauce_1, basket_1_contain_region); open(wooden_cabinet_1_middle_region)` | [PNG](comparison_png/VCN19_005__put_the_tomato_sauce_in_the_basket_then_open_the_middle_drawer_of_the_wooden_cabinet.png) |
| `VCN19_007` | 3 | `true` | Put the cream cheese on the stove, then turn on the stove, then put the tomato sauce in the basket. | `on(cream_cheese_1, flat_stove_1_cook_region); turnon(flat_stove_1); in(tomato_sauce_1, basket_1_contain_region)` | [PNG](comparison_png/VCN19_007__put_the_cream_cheese_on_the_stove_then_turn_on_the_stove_then_put_the_tomato_sauce_in_the_basket.png) |
| `VCN19_008` | 2 | `true` | Pick up the ramekin on the cookies box and place it on the plate, then turn on the stove. | `on(glazed_rim_porcelain_ramekin_1, plate_1); turnon(flat_stove_1)` | [PNG](comparison_png/VCN19_008__pick_up_the_ramekin_on_the_cookies_box_and_place_it_on_the_plate_then_turn_on_the_stove.png) |
| `VCN19_009` | 3 | `true` | Put the chocolate pudding on the black bowl, then open the middle drawer of the cabinet, then put the loaded black bowl on top of the wooden cabinet. | `on(chocolate_pudding_1, akita_black_bowl_1); open(wooden_cabinet_1_middle_region); on(akita_black_bowl_1, wooden_cabinet_1_top_side)` | [PNG](comparison_png/VCN19_009__put_the_chocolate_pudding_on_the_black_bowl_then_open_the_middle_drawer_of_the_cabinet_then_put_the_loaded_black_bowl_on_top_of_the_wooden_cabinet.png) |
| `VCN19_010` | 2 | `true` | Open the middle drawer of the wooden cabinet, then put the ramekin on the plate. | `open(wooden_cabinet_1_middle_region); on(glazed_rim_porcelain_ramekin_1, plate_1)` | [PNG](comparison_png/VCN19_010__open_the_middle_drawer_of_the_wooden_cabinet_then_put_the_ramekin_on_the_plate.png) |
| `VCN19_011` | 2 | `true` | Put the cream cheese on the plate, then push the loaded plate to the front of the stove. | `on(cream_cheese_1, plate_1); on(plate_1, main_table_stove_front_region)` | [PNG](comparison_png/VCN19_011__put_the_cream_cheese_on_the_plate_then_push_the_loaded_plate_to_the_front_of_the_stove.png) |
| `VCN19_012` | 3 | `true` | Put the butter on the plate, then push the loaded plate to the front of the stove, then open the middle drawer of the wooden cabinet. | `on(butter_1, plate_1); on(plate_1, main_table_stove_front_region); open(wooden_cabinet_1_middle_region)` | [PNG](comparison_png/VCN19_012__put_the_butter_on_the_plate_then_push_the_loaded_plate_to_the_front_of_the_stove_then_open_the_middle_drawer_of_the_wooden_cabinet.png) |
| `VCN19_013` | 3 | `true` | Put the butter on the plate, then push the loaded plate to the front of the stove, then turn on the stove. | `on(butter_1, plate_1); on(plate_1, main_table_stove_front_region); turnon(flat_stove_1)` | [PNG](comparison_png/VCN19_013__put_the_butter_on_the_plate_then_push_the_loaded_plate_to_the_front_of_the_stove_then_turn_on_the_stove.png) |
| `VCN19_014` | 3 | `true` | Put the cream cheese on the plate, then push the loaded plate to the front of the stove, then open the bottom drawer of the wooden cabinet. | `on(cream_cheese_1, plate_1); on(plate_1, main_table_stove_front_region); open(wooden_cabinet_1_bottom_region)` | [PNG](comparison_png/VCN19_014__put_the_cream_cheese_on_the_plate_then_push_the_loaded_plate_to_the_front_of_the_stove_then_open_the_bottom_drawer_of_the_wooden_cabinet.png) |
| `VCN19_015` | 2 | `true` | Put the plate on top of the wooden cabinet, then put the cream cheese in the basket. | `on(plate_1, wooden_cabinet_1_top_side); in(cream_cheese_1, basket_1_contain_region)` | [PNG](comparison_png/VCN19_015__put_the_plate_on_top_of_the_wooden_cabinet_then_put_the_cream_cheese_in_the_basket.png) |
| `VCN19_016` | 3 | `true` | Put the cream cheese on the stove, then turn on the stove, then put the ramekin on the plate. | `on(cream_cheese_1, flat_stove_1_cook_region); turnon(flat_stove_1); on(glazed_rim_porcelain_ramekin_1, plate_1)` | [PNG](comparison_png/VCN19_016__put_the_cream_cheese_on_the_stove_then_turn_on_the_stove_then_put_the_ramekin_on_the_plate.png) |
| `VCN19_017` | 3 | `true` | Put the cream cheese on the stove, then turn on the stove, then close the top drawer of the wooden cabinet. | `on(cream_cheese_1, flat_stove_1_cook_region); turnon(flat_stove_1); close(wooden_cabinet_1_top_region)` | [PNG](comparison_png/VCN19_017__put_the_cream_cheese_on_the_stove_then_turn_on_the_stove_then_close_the_top_drawer_of_the_wooden_cabinet.png) |
| `VCN19_019` | 2 | `true` | Pick up the ramekin on the cookies box and place it on the plate, then open the bottom drawer of the wooden cabinet. | `on(glazed_rim_porcelain_ramekin_1, plate_1); open(wooden_cabinet_1_bottom_region)` | [PNG](comparison_png/VCN19_019__pick_up_the_ramekin_on_the_cookies_box_and_place_it_on_the_plate_then_open_the_bottom_drawer_of_the_wooden_cabinet.png) |
| `VCN19_020` | 2 | `true` | Open the top drawer of the wooden cabinet, then put the ramekin on the plate. | `open(wooden_cabinet_1_top_region); on(glazed_rim_porcelain_ramekin_1, plate_1)` | [PNG](comparison_png/VCN19_020__open_the_top_drawer_of_the_wooden_cabinet_then_put_the_ramekin_on_the_plate.png) |
