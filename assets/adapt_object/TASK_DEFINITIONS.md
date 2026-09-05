# DifferentTargetSameLayout — exhaustive task definitions

Generated 2026-08-31 from the ten original LIBERO-Object layouts.

## Definition rule

- Preserve the original LIBERO-Object BDDL regions, objects, every `On(...)` init atom, basket pose, and pruned init states.
- Choose each of the five original distractors once as the new goal target.
- Change only task language, `obj_of_interest`, and `In(new_target, basket)` goal.
- This differs from legacy `OGTOBJI_001..050`, which moved the substitute target into the original target slot by swapping object identities/regions.

## Exhaustive audit

| Set | Count | Meaning |
|---|---:|---|
| All physical candidates | 50 | 10 layouts × 5 non-original targets |
| Seen target-interaction region | 10 | new target remains in region 0, which is a target region in five other stock tasks |
| Distractor-only region | 40 | position appeared in stock layout, but not evidenced as an original target-grasp region |
| Same source+goal as current ReFinal | 9 | different physical init arrangement; tagged for conservative filtering |
| Exact physical duplicates with current ReFinal/full150 | 0 | compared by regions + complete init mapping + goal target |

## Evaluation subsets

- `all50`: every candidate.
- `seen10`: controlled position subset with original target-interaction evidence.
- `strict41`: excludes the nine source-layout+goal pairs already represented in current ReFinal, even though physical poses differ.
- `seen_strict9`: intersection of `seen10` and `strict41`.

## Tasks

| # | Task ID | Source layout target | New task instruction | Region | Position evidence | Current source+goal overlap | PNG |
|---:|---|---|---|---|---|---|---|
| 1 | `OGDTSL_001` | alphabet soup | Pick the salad dressing and place it in the basket | `floor_other_object_region_0` (+0.050, -0.100) | seen_target_interaction_region | `-` | [compare](comparison_png/OGDTSL_001__alphabet_soup_to_salad_dressing.png) |
| 2 | `OGDTSL_002` | alphabet soup | Pick the cream cheese and place it in the basket | `floor_other_object_region_1` (-0.150, +0.060) | original_distractor_only_region | `-` | [compare](comparison_png/OGDTSL_002__alphabet_soup_to_cream_cheese.png) |
| 3 | `OGDTSL_003` | alphabet soup | Pick the milk and place it in the basket | `floor_other_object_region_2` (+0.100, -0.200) | original_distractor_only_region | `-` | [compare](comparison_png/OGDTSL_003__alphabet_soup_to_milk.png) |
| 4 | `OGDTSL_004` | alphabet soup | Pick the tomato sauce and place it in the basket | `floor_other_object_region_3` (+0.150, +0.030) | original_distractor_only_region | `-` | [compare](comparison_png/OGDTSL_004__alphabet_soup_to_tomato_sauce.png) |
| 5 | `OGDTSL_005` | alphabet soup | Pick the butter and place it in the basket | `floor_other_object_region_4` (-0.200, -0.080) | original_distractor_only_region | `-` | [compare](comparison_png/OGDTSL_005__alphabet_soup_to_butter.png) |
| 6 | `OGDTSL_006` | bbq sauce | Pick the chocolate pudding and place it in the basket | `floor_other_object_region_0` (-0.120, -0.240) | seen_target_interaction_region | `-` | [compare](comparison_png/OGDTSL_006__bbq_sauce_to_chocolate_pudding.png) |
| 7 | `OGDTSL_007` | bbq sauce | Pick the ketchup and place it in the basket | `floor_other_object_region_1` (-0.150, +0.060) | original_distractor_only_region | `-` | [compare](comparison_png/OGDTSL_007__bbq_sauce_to_ketchup.png) |
| 8 | `OGDTSL_008` | bbq sauce | Pick the salad dressing and place it in the basket | `floor_other_object_region_2` (+0.100, -0.200) | original_distractor_only_region | `-` | [compare](comparison_png/OGDTSL_008__bbq_sauce_to_salad_dressing.png) |
| 9 | `OGDTSL_009` | bbq sauce | Pick the alphabet soup and place it in the basket | `floor_other_object_region_3` (+0.150, +0.030) | original_distractor_only_region | `-` | [compare](comparison_png/OGDTSL_009__bbq_sauce_to_alphabet_soup.png) |
| 10 | `OGDTSL_010` | bbq sauce | Pick the cream cheese and place it in the basket | `floor_other_object_region_4` (-0.200, -0.080) | original_distractor_only_region | `-` | [compare](comparison_png/OGDTSL_010__bbq_sauce_to_cream_cheese.png) |
| 11 | `OGDTSL_011` | butter | Pick the tomato sauce and place it in the basket | `floor_other_object_region_0` (+0.050, -0.100) | seen_target_interaction_region | `-` | [compare](comparison_png/OGDTSL_011__butter_to_tomato_sauce.png) |
| 12 | `OGDTSL_012` | butter | Pick the orange juice and place it in the basket | `floor_other_object_region_1` (-0.150, +0.060) | original_distractor_only_region | `-` | [compare](comparison_png/OGDTSL_012__butter_to_orange_juice.png) |
| 13 | `OGDTSL_013` | butter | Pick the chocolate pudding and place it in the basket | `floor_other_object_region_2` (+0.100, -0.200) | original_distractor_only_region | `OGTOBJI_033` | [compare](comparison_png/OGDTSL_013__butter_to_chocolate_pudding.png) |
| 14 | `OGDTSL_014` | butter | Pick the bbq sauce and place it in the basket | `floor_other_object_region_3` (+0.150, +0.030) | original_distractor_only_region | `-` | [compare](comparison_png/OGDTSL_014__butter_to_bbq_sauce.png) |
| 15 | `OGDTSL_015` | butter | Pick the ketchup and place it in the basket | `floor_other_object_region_4` (-0.200, -0.080) | original_distractor_only_region | `-` | [compare](comparison_png/OGDTSL_015__butter_to_ketchup.png) |
| 16 | `OGDTSL_016` | chocolate pudding | Pick the orange juice and place it in the basket | `floor_other_object_region_0` (+0.050, -0.100) | seen_target_interaction_region | `-` | [compare](comparison_png/OGDTSL_016__chocolate_pudding_to_orange_juice.png) |
| 17 | `OGDTSL_017` | chocolate pudding | Pick the bbq sauce and place it in the basket | `floor_other_object_region_1` (-0.150, +0.060) | original_distractor_only_region | `-` | [compare](comparison_png/OGDTSL_017__chocolate_pudding_to_bbq_sauce.png) |
| 18 | `OGDTSL_018` | chocolate pudding | Pick the ketchup and place it in the basket | `floor_other_object_region_2` (+0.100, -0.200) | original_distractor_only_region | `-` | [compare](comparison_png/OGDTSL_018__chocolate_pudding_to_ketchup.png) |
| 19 | `OGDTSL_019` | chocolate pudding | Pick the salad dressing and place it in the basket | `floor_other_object_region_3` (+0.150, +0.030) | original_distractor_only_region | `-` | [compare](comparison_png/OGDTSL_019__chocolate_pudding_to_salad_dressing.png) |
| 20 | `OGDTSL_020` | chocolate pudding | Pick the alphabet soup and place it in the basket | `floor_other_object_region_4` (-0.200, -0.080) | original_distractor_only_region | `-` | [compare](comparison_png/OGDTSL_020__chocolate_pudding_to_alphabet_soup.png) |
| 21 | `OGDTSL_021` | cream cheese | Pick the alphabet soup and place it in the basket | `floor_other_object_region_0` (-0.120, -0.240) | seen_target_interaction_region | `-` | [compare](comparison_png/OGDTSL_021__cream_cheese_to_alphabet_soup.png) |
| 22 | `OGDTSL_022` | cream cheese | Pick the milk and place it in the basket | `floor_other_object_region_1` (-0.150, +0.060) | original_distractor_only_region | `-` | [compare](comparison_png/OGDTSL_022__cream_cheese_to_milk.png) |
| 23 | `OGDTSL_023` | cream cheese | Pick the tomato sauce and place it in the basket | `floor_other_object_region_2` (+0.100, -0.200) | original_distractor_only_region | `-` | [compare](comparison_png/OGDTSL_023__cream_cheese_to_tomato_sauce.png) |
| 24 | `OGDTSL_024` | cream cheese | Pick the butter and place it in the basket | `floor_other_object_region_3` (+0.150, +0.030) | original_distractor_only_region | `OGTOBJI_009` | [compare](comparison_png/OGDTSL_024__cream_cheese_to_butter.png) |
| 25 | `OGDTSL_025` | cream cheese | Pick the orange juice and place it in the basket | `floor_other_object_region_4` (-0.200, -0.080) | original_distractor_only_region | `-` | [compare](comparison_png/OGDTSL_025__cream_cheese_to_orange_juice.png) |
| 26 | `OGDTSL_026` | ketchup | Pick the bbq sauce and place it in the basket | `floor_other_object_region_0` (+0.050, -0.100) | seen_target_interaction_region | `-` | [compare](comparison_png/OGDTSL_026__ketchup_to_bbq_sauce.png) |
| 27 | `OGDTSL_027` | ketchup | Pick the salad dressing and place it in the basket | `floor_other_object_region_1` (-0.150, +0.060) | original_distractor_only_region | `-` | [compare](comparison_png/OGDTSL_027__ketchup_to_salad_dressing.png) |
| 28 | `OGDTSL_028` | ketchup | Pick the alphabet soup and place it in the basket | `floor_other_object_region_2` (+0.100, -0.200) | original_distractor_only_region | `OGTOBJI_023` | [compare](comparison_png/OGDTSL_028__ketchup_to_alphabet_soup.png) |
| 29 | `OGDTSL_029` | ketchup | Pick the cream cheese and place it in the basket | `floor_other_object_region_3` (+0.150, +0.030) | original_distractor_only_region | `OGTOBJI_024` | [compare](comparison_png/OGDTSL_029__ketchup_to_cream_cheese.png) |
| 30 | `OGDTSL_030` | ketchup | Pick the milk and place it in the basket | `floor_other_object_region_4` (-0.200, -0.080) | original_distractor_only_region | `OGTOBJI_025` | [compare](comparison_png/OGDTSL_030__ketchup_to_milk.png) |
| 31 | `OGDTSL_031` | milk | Pick the cream cheese and place it in the basket | `floor_other_object_region_0` (+0.050, -0.100) | seen_target_interaction_region | `-` | [compare](comparison_png/OGDTSL_031__milk_to_cream_cheese.png) |
| 32 | `OGDTSL_032` | milk | Pick the tomato sauce and place it in the basket | `floor_other_object_region_1` (-0.150, +0.060) | original_distractor_only_region | `-` | [compare](comparison_png/OGDTSL_032__milk_to_tomato_sauce.png) |
| 33 | `OGDTSL_033` | milk | Pick the butter and place it in the basket | `floor_other_object_region_2` (+0.100, -0.200) | original_distractor_only_region | `-` | [compare](comparison_png/OGDTSL_033__milk_to_butter.png) |
| 34 | `OGDTSL_034` | milk | Pick the orange juice and place it in the basket | `floor_other_object_region_3` (+0.150, +0.030) | original_distractor_only_region | `-` | [compare](comparison_png/OGDTSL_034__milk_to_orange_juice.png) |
| 35 | `OGDTSL_035` | milk | Pick the chocolate pudding and place it in the basket | `floor_other_object_region_4` (-0.200, -0.080) | original_distractor_only_region | `-` | [compare](comparison_png/OGDTSL_035__milk_to_chocolate_pudding.png) |
| 36 | `OGDTSL_036` | orange juice | Pick the butter and place it in the basket | `floor_other_object_region_0` (-0.120, -0.240) | seen_target_interaction_region | `-` | [compare](comparison_png/OGDTSL_036__orange_juice_to_butter.png) |
| 37 | `OGDTSL_037` | orange juice | Pick the chocolate pudding and place it in the basket | `floor_other_object_region_1` (-0.150, +0.060) | original_distractor_only_region | `-` | [compare](comparison_png/OGDTSL_037__orange_juice_to_chocolate_pudding.png) |
| 38 | `OGDTSL_038` | orange juice | Pick the bbq sauce and place it in the basket | `floor_other_object_region_2` (+0.100, -0.200) | original_distractor_only_region | `-` | [compare](comparison_png/OGDTSL_038__orange_juice_to_bbq_sauce.png) |
| 39 | `OGDTSL_039` | orange juice | Pick the ketchup and place it in the basket | `floor_other_object_region_3` (+0.150, +0.030) | original_distractor_only_region | `-` | [compare](comparison_png/OGDTSL_039__orange_juice_to_ketchup.png) |
| 40 | `OGDTSL_040` | orange juice | Pick the salad dressing and place it in the basket | `floor_other_object_region_4` (-0.200, -0.080) | original_distractor_only_region | `-` | [compare](comparison_png/OGDTSL_040__orange_juice_to_salad_dressing.png) |
| 41 | `OGDTSL_041` | salad dressing | Pick the ketchup and place it in the basket | `floor_other_object_region_0` (-0.120, -0.240) | seen_target_interaction_region | `OGTOBJI_011` | [compare](comparison_png/OGDTSL_041__salad_dressing_to_ketchup.png) |
| 42 | `OGDTSL_042` | salad dressing | Pick the alphabet soup and place it in the basket | `floor_other_object_region_1` (-0.150, +0.060) | original_distractor_only_region | `-` | [compare](comparison_png/OGDTSL_042__salad_dressing_to_alphabet_soup.png) |
| 43 | `OGDTSL_043` | salad dressing | Pick the cream cheese and place it in the basket | `floor_other_object_region_2` (+0.100, -0.200) | original_distractor_only_region | `-` | [compare](comparison_png/OGDTSL_043__salad_dressing_to_cream_cheese.png) |
| 44 | `OGDTSL_044` | salad dressing | Pick the milk and place it in the basket | `floor_other_object_region_3` (+0.150, +0.030) | original_distractor_only_region | `-` | [compare](comparison_png/OGDTSL_044__salad_dressing_to_milk.png) |
| 45 | `OGDTSL_045` | salad dressing | Pick the tomato sauce and place it in the basket | `floor_other_object_region_4` (-0.200, -0.080) | original_distractor_only_region | `OGTOBJI_015` | [compare](comparison_png/OGDTSL_045__salad_dressing_to_tomato_sauce.png) |
| 46 | `OGDTSL_046` | tomato sauce | Pick the milk and place it in the basket | `floor_other_object_region_0` (-0.120, -0.240) | seen_target_interaction_region | `-` | [compare](comparison_png/OGDTSL_046__tomato_sauce_to_milk.png) |
| 47 | `OGDTSL_047` | tomato sauce | Pick the butter and place it in the basket | `floor_other_object_region_1` (-0.150, +0.060) | original_distractor_only_region | `-` | [compare](comparison_png/OGDTSL_047__tomato_sauce_to_butter.png) |
| 48 | `OGDTSL_048` | tomato sauce | Pick the orange juice and place it in the basket | `floor_other_object_region_2` (+0.100, -0.200) | original_distractor_only_region | `OGTOBJI_028` | [compare](comparison_png/OGDTSL_048__tomato_sauce_to_orange_juice.png) |
| 49 | `OGDTSL_049` | tomato sauce | Pick the chocolate pudding and place it in the basket | `floor_other_object_region_3` (+0.150, +0.030) | original_distractor_only_region | `-` | [compare](comparison_png/OGDTSL_049__tomato_sauce_to_chocolate_pudding.png) |
| 50 | `OGDTSL_050` | tomato sauce | Pick the bbq sauce and place it in the basket | `floor_other_object_region_4` (-0.200, -0.080) | original_distractor_only_region | `OGTOBJI_030` | [compare](comparison_png/OGDTSL_050__tomato_sauce_to_bbq_sauce.png) |

## Validation

- All 50 task IDs, canonical signatures, normalized BDDL files, and physical fingerprints are unique.
- Candidate init mappings and pruned simulator states match the corresponding original LIBERO-Object task.
- No candidate physical fingerprint matches an active ReFinal task or a task in the original LIBERO-EX 150 bundle.
- The RAIN benchmark loader resolves all50/seen10/strict41/seen_strict9 in manifest order and builds action plans/conditions for every task.
- Comparison PNGs intentionally show identical left/right physical pixels; only the instructed goal target changes.
