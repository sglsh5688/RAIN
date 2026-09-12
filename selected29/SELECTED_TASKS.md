# Selected LIBERO-EX tasks

Selection updated 2026-09-11. 20 Decomposition + 20 Adapt + 20 Compose (60 total).

User-authorized replacements: VCN91_002 → CTR_176 (5/5); SPBSC_001 → CTR_140 (1/5); BDRCOMP_021 → CTR_103 (4/5). All other 57 selected tasks and results are unchanged.

RAIN Compose: **50/100**. All historical selected RAIN records: **706/1050**, with **208 saved success clips**. Original episode counts and task-specific protocols remain unchanged. No policy reruns were performed for this selection update.

Separate π0.5 LIBERO-40 evaluation: **56/60 tasks**, **75/280 episodes (26.8%)**, 20 successful tasks. Decomposition 7/100; Adapt 58/100; Compose 10/80 (16/20 evaluated). Pending: CTR_103, BDRMIN_002, CTR_176, CTR_140. The retired BDRCOMP_021 0/5 result is excluded from current aggregates and retained in the historical snapshot/source ledger. ANLGX_023 retains its corrected strict close-only 0/5 result.

The historical source metadata and review evidence retain their original pre-selection status. Each incoming bundle has a separate `SELECTION_OVERLAY.json` recording current selection. Task/init/rule source bytes and evaluation outcomes are unchanged.

This release contains definitions and evaluation evidence, plus local runtime source exports for the three incoming tasks; external model/framework dependencies are not bundled. The declared ordered/contact rules require their evaluator runtimes; BDDL alone is insufficient.

Current descriptions updated 2026-09-12: all 60 omit terminal periods. Adapt_009 names the robot-right caddy compartment while retaining the rotated caddy’s native left_contain_region physical goal. Compose_019 retains its explicit three-placement order. The [current task review](../task_review/index.html) and current definition links below use these descriptions. Historical source instructions, videos, episode counts and evaluation outcomes are unchanged; the new wording does not describe what earlier evaluations received.

Bowl-drainer native region names and coordinates remain unchanged (left_region: local +Y; right_region: local −Y). Compose_015 uses the user-requested robot-arm wording **butter RIGHT → tomato sauce LEFT**, mapped to the preserved internal goals **butter → left_region; tomato sauce → right_region**. Compose_018 keeps **alphabet soup RIGHT → tomato sauce LEFT**, mapped to its existing **right_region → left_region** goals. Historical instructions, source conditioning and evaluation results retain their recorded wording. See [현재 지시문 · 원본 구획 비교](../task_review/DRAINER_DIRECTIONS.png). Current per-stage views and historical comparisons are linked separately:

| Current task | Legacy ID | Current scene and masks | Historical comparison |
|---|---|---|---|
| Adapt_017 | BDRSWAP_001 | [Current view](../task_review/scenes/Adapt/Adapt_017/TASK_REVIEW.png) | [Historical image](assets/comparison_png/BDRSWAP_001.png) — This historical image uses the opposite horizontal orientation; native right appears on the image-left side of the drainer. |
| Compose_015 | CTR_103 | [Current view](../task_review/scenes/Compose/Compose_015/TASK_REVIEW.png) | [Historical image](assets/comparison_png/CTR_103.png) — This historical image combines both compartment masks, so the two placement stages are not shown separately. |
| Compose_018 | BDRMIN_002 | [Current view](../task_review/scenes/Compose/Compose_018/TASK_REVIEW.png) | [Historical image](assets/comparison_png/BDRMIN_002.png) — This historical image uses the opposite horizontal orientation; native right appears on the image-left side of the drainer. |

Caddy frame guide: The caddy is rotated 180°: its native left_contain_region is on the robot’s right. The physical goal and scene are unchanged. The conditioning mask covers the whole caddy; use the named goal region and scene to distinguish the compartment. See [compartment coordinate frames](../task_review/COMPARTMENT_FRAMES.png). [Adapt_009 current scene and masks](../task_review/scenes/Adapt/Adapt_009/TASK_REVIEW.png) · [Historical comparison](assets/comparison_png/ANLGX_178.png).

Every task below links its current BDDL and metadata. The [historical task-definition archive](task_bundles.zip) retains the original evaluation wording.

## Decomposition

| Task ID | Current instruction | Historical RAIN SR | π0.5 LIBERO-40 SR (5ep) | Current definitions |
|---|---|---|---|---|
| TDL10_001 | Put the white mug on the left plate | 33/50 (66.0%) | 0/5 (0%) | [BDDL](../task_review/definitions/Decomposition_001/task.bddl) · [Metadata](../task_review/definitions/Decomposition_001/task_meta.yaml) |
| TDL10_002 | Put the yellow and white mug on the right plate | 50/50 (100.0%) | 0/5 (0%) | [BDDL](../task_review/definitions/Decomposition_002/task.bddl) · [Metadata](../task_review/definitions/Decomposition_002/task_meta.yaml) |
| TDL10_003 | Put the white mug on the plate | 14/50 (28.0%) | 0/5 (0%) | [BDDL](../task_review/definitions/Decomposition_003/task.bddl) · [Metadata](../task_review/definitions/Decomposition_003/task_meta.yaml) |
| TDL10_004 | Put the chocolate pudding to the right of the plate | 49/50 (98.0%) | 0/5 (0%) | [BDDL](../task_review/definitions/Decomposition_004/task.bddl) · [Metadata](../task_review/definitions/Decomposition_004/task_meta.yaml) |
| TDL10_005 | Put the yellow and white mug in the microwave | 20/50 (40.0%) | 0/5 (0%) | [BDDL](../task_review/definitions/Decomposition_005/task.bddl) · [Metadata](../task_review/definitions/Decomposition_005/task_meta.yaml) |
| TDL10_006 | Close the microwave | 47/50 (94.0%) | 1/5 (20%) | [BDDL](../task_review/definitions/Decomposition_006/task.bddl) · [Metadata](../task_review/definitions/Decomposition_006/task_meta.yaml) |
| TDL10_008 | Put the moka pot on the stove | 10/50 (20.0%) | 0/5 (0%) | [BDDL](../task_review/definitions/Decomposition_007/task.bddl) · [Metadata](../task_review/definitions/Decomposition_007/task_meta.yaml) |
| TDL10_009 | Put the alphabet soup in the basket | 50/50 (100.0%) | 0/5 (0%) | [BDDL](../task_review/definitions/Decomposition_008/task.bddl) · [Metadata](../task_review/definitions/Decomposition_008/task_meta.yaml) |
| TDL10_010 | Put the cream cheese box in the basket | 41/50 (82.0%) | 0/5 (0%) | [BDDL](../task_review/definitions/Decomposition_009/task.bddl) · [Metadata](../task_review/definitions/Decomposition_009/task_meta.yaml) |
| TDL10_011 | Put the alphabet soup in the basket | 45/50 (90.0%) | 0/5 (0%) | [BDDL](../task_review/definitions/Decomposition_010/task.bddl) · [Metadata](../task_review/definitions/Decomposition_010/task_meta.yaml) |
| TDL10_012 | Put the tomato sauce in the basket | 48/50 (96.0%) | 0/5 (0%) | [BDDL](../task_review/definitions/Decomposition_011/task.bddl) · [Metadata](../task_review/definitions/Decomposition_011/task_meta.yaml) |
| TDL10_013 | Put the cream cheese box in the basket | 22/50 (44.0%) | 0/5 (0%) | [BDDL](../task_review/definitions/Decomposition_012/task.bddl) · [Metadata](../task_review/definitions/Decomposition_012/task_meta.yaml) |
| TDL10_014 | Put the butter in the basket | 50/50 (100.0%) | 0/5 (0%) | [BDDL](../task_review/definitions/Decomposition_013/task.bddl) · [Metadata](../task_review/definitions/Decomposition_013/task_meta.yaml) |
| TDL10_016 | Close the bottom drawer of the cabinet | 16/50 (32.0%) | 0/5 (0%) | [BDDL](../task_review/definitions/Decomposition_014/task.bddl) · [Metadata](../task_review/definitions/Decomposition_014/task_meta.yaml) |
| TDC40_001 | Turn on the stove | 2/10 (20.0%) | 0/5 (0%) | [BDDL](../task_review/definitions/Decomposition_015/task.bddl) · [Metadata](../task_review/definitions/Decomposition_015/task_meta.yaml) |
| TDC40_002 | Put the black bowl in the bottom drawer of the cabinet | 0/10 (0.0%) | 0/5 (0%) | [BDDL](../task_review/definitions/Decomposition_016/task.bddl) · [Metadata](../task_review/definitions/Decomposition_016/task_meta.yaml) |
| TDC40_003 | Put the left moka pot on the stove | 9/10 (90.0%) | 2/5 (40%) | [BDDL](../task_review/definitions/Decomposition_017/task.bddl) · [Metadata](../task_review/definitions/Decomposition_017/task_meta.yaml) |
| TDC40_004 | Put the right moka pot on the stove | 0/10 (0.0%) | 0/5 (0%) | [BDDL](../task_review/definitions/Decomposition_018/task.bddl) · [Metadata](../task_review/definitions/Decomposition_018/task_meta.yaml) |
| TDC40_005 | Open the top drawer of the cabinet | 1/10 (10.0%) | 0/5 (0%) | [BDDL](../task_review/definitions/Decomposition_019/task.bddl) · [Metadata](../task_review/definitions/Decomposition_019/task_meta.yaml) |
| TDC40_006 | Put the black bowl inside the top drawer of the cabinet | 10/10 (100.0%) | 4/5 (80%) | [BDDL](../task_review/definitions/Decomposition_020/task.bddl) · [Metadata](../task_review/definitions/Decomposition_020/task_meta.yaml) |

## Adapt

| Task ID | Current instruction | Historical RAIN SR | π0.5 LIBERO-40 SR (5ep) | Current definitions |
|---|---|---|---|---|
| ANLGX_002 | Put the white mug on the middle plate | 4/5 (80.0%) | 4/5 (80%) | [BDDL](../task_review/definitions/Adapt_001/task.bddl) · [Metadata](../task_review/definitions/Adapt_001/task_meta.yaml) |
| ANLGX_003 | Put the white mug on the right plate | 3/5 (60.0%) | 0/5 (0%) | [BDDL](../task_review/definitions/Adapt_002/task.bddl) · [Metadata](../task_review/definitions/Adapt_002/task_meta.yaml) |
| ANLGX_017 | Put the black bowl in the middle drawer of the white cabinet | 5/5 (100.0%) | 5/5 (100%) | [BDDL](../task_review/definitions/Adapt_003/task.bddl) · [Metadata](../task_review/definitions/Adapt_003/task_meta.yaml) |
| ANLGX_022 | Close the top drawer of the white cabinet | 4/5 (80.0%) | 0/5 (0%) | [BDDL](../task_review/definitions/Adapt_004/task.bddl) · [Metadata](../task_review/definitions/Adapt_004/task_meta.yaml) |
| ANLGX_023 | Close the middle drawer of the white cabinet | 4/5 (80.0%) | 0/5 (0%) | [BDDL](../task_review/definitions/Adapt_005/task.bddl) · [Metadata](../task_review/definitions/Adapt_005/task_meta.yaml) |
| ANLGX_089 | Pick up the wine bottle at the table center and place it on the plate | 3/5 (60.0%) | 2/5 (40%) | [BDDL](../task_review/definitions/Adapt_006/task.bddl) · [Metadata](../task_review/definitions/Adapt_006/task_meta.yaml) |
| ANLGX_134 | Put the plate on the top of the wooden cabinet | 1/5 (20.0%) | 0/5 (0%) | [BDDL](../task_review/definitions/Adapt_007/task.bddl) · [Metadata](../task_review/definitions/Adapt_007/task_meta.yaml) |
| ANLGX_147 | Put the cream cheese in the top drawer of the wooden cabinet | 3/5 (60.0%) | 3/5 (60%) | [BDDL](../task_review/definitions/Adapt_008/task.bddl) · [Metadata](../task_review/definitions/Adapt_008/task_meta.yaml) |
| ANLGX_178 | Put the yellow and white mug in the right compartment of the caddy | 3/5 (60.0%) | 0/5 (0%) | [BDDL](../task_review/definitions/Adapt_009/task.bddl) · [Metadata](../task_review/definitions/Adapt_009/task_meta.yaml) |
| OGTS_001 | Pick the alphabet soup and place it in the basket | 48/50 (96.0%) | 4/5 (80%) | [BDDL](../task_review/definitions/Adapt_010/task.bddl) · [Metadata](../task_review/definitions/Adapt_010/task_meta.yaml) |
| OGTS_010 | Pick the orange juice and place it in the basket | 26/50 (52.0%) | 0/5 (0%) | [BDDL](../task_review/definitions/Adapt_011/task.bddl) · [Metadata](../task_review/definitions/Adapt_011/task_meta.yaml) |
| OGDTSL_011 | Pick the tomato sauce and place it in the basket | 4/5 (80.0%) | 5/5 (100%) | [BDDL](../task_review/definitions/Adapt_012/task.bddl) · [Metadata](../task_review/definitions/Adapt_012/task_meta.yaml) |
| OGDTSL_046 | Pick the milk and place it in the basket | 2/5 (40.0%) | 5/5 (100%) | [BDDL](../task_review/definitions/Adapt_013/task.bddl) · [Metadata](../task_review/definitions/Adapt_013/task_meta.yaml) |
| NAFR3_001 | Put the popcorn on top of the short fridge | 4/5 (80%) | 2/5 (40%) | [BDDL](../task_review/definitions/Adapt_014/task.bddl) · [Metadata](../task_review/definitions/Adapt_014/task_meta.yaml) |
| NAFR3_002 | Put the yellow book on top of the two-layer wooden shelf | 4/5 (80%) | 5/5 (100%) | [BDDL](../task_review/definitions/Adapt_015/task.bddl) · [Metadata](../task_review/definitions/Adapt_015/task_meta.yaml) |
| DSET_001 | Pick up the black bowl at the table center and place it on the dining-set mat | 5/5 (100.0%) | 5/5 (100%) | [BDDL](../task_review/definitions/Adapt_016/task.bddl) · [Metadata](../task_review/definitions/Adapt_016/task_meta.yaml) |
| BDRSWAP_001 | Pick the alphabet soup and place it in the right compartment of the bowl drainer | 5/5 (100%) | 5/5 (100%) | [BDDL](../task_review/definitions/Adapt_017/task.bddl) · [Metadata](../task_review/definitions/Adapt_017/task_meta.yaml) |
| ADVCN19_001 | Open the top drawer of the wooden cabinet | 4/5 (80%) | 4/5 (80%) | [BDDL](../task_review/definitions/Adapt_018/task.bddl) · [Metadata](../task_review/definitions/Adapt_018/task_meta.yaml) |
| WTRAYR_004 | Pick up the black bowl and place it in the wooden tray | 2/5 (40.0%) | 5/5 (100%) | [BDDL](../task_review/definitions/Adapt_019/task.bddl) · [Metadata](../task_review/definitions/Adapt_019/task_meta.yaml) |
| GRACK_002 | Put the ketchup on the rack | 5/5 (100.0%) | 4/5 (80%) | [BDDL](../task_review/definitions/Adapt_020/task.bddl) · [Metadata](../task_review/definitions/Adapt_020/task_meta.yaml) |

## Compose

| Task ID | Current instruction | Historical RAIN SR | π0.5 LIBERO-40 SR (5ep) | Current definitions |
|---|---|---|---|---|
| VCN8_008 | Put the chocolate pudding on the black bowl, then open the middle drawer of the cabinet | 4/5 (80%) | 0/5 (0%) | [BDDL](../task_review/definitions/Compose_001/task.bddl) · [Metadata](../task_review/definitions/Compose_001/task_meta.yaml) |
| VCN9_010 | Put the cream cheese on the stove, then turn on the stove | 4/5 (80%) | 0/5 (0%) | [BDDL](../task_review/definitions/Compose_002/task.bddl) · [Metadata](../task_review/definitions/Compose_002/task_meta.yaml) |
| VCN10_001 | Put the cream cheese on the stove, then push the plate to the front of the stove | 2/5 (40%) | 0/5 (0%) | [BDDL](../task_review/definitions/Compose_003/task.bddl) · [Metadata](../task_review/definitions/Compose_003/task_meta.yaml) |
| VCN19_020 | Open the top drawer of the wooden cabinet, then put the ramekin on the plate | 1/5 (20%) | 3/5 (60%) | [BDDL](../task_review/definitions/Compose_004/task.bddl) · [Metadata](../task_review/definitions/Compose_004/task_meta.yaml) |
| VCN21_001 | Put the moka pot on the stove, then close the microwave door | 4/5 (80%) | 4/5 (80%) | [BDDL](../task_review/definitions/Compose_005/task.bddl) · [Metadata](../task_review/definitions/Compose_005/task_meta.yaml) |
| COMP2_012 | Put the butter in the basket, and then put the tomato sauce in the basket | 5/5 (100.0%) | 0/5 (0%) | [BDDL](../task_review/definitions/Compose_006/task.bddl) · [Metadata](../task_review/definitions/Compose_006/task_meta.yaml) |
| COMP2_032 | Push the plate to the front of the stove, and then open the middle drawer of the cabinet | 1/5 (20.0%) | 0/5 (0%) | [BDDL](../task_review/definitions/Compose_007/task.bddl) · [Metadata](../task_review/definitions/Compose_007/task_meta.yaml) |
| COMP2_222 | Put the alphabet soup in the basket, and then put the tomato sauce in the basket | 1/5 (20.0%) | 0/5 (0%) | [BDDL](../task_review/definitions/Compose_008/task.bddl) · [Metadata](../task_review/definitions/Compose_008/task_meta.yaml) |
| COMP2_303 | Put the milk in the basket, and then put the cream cheese box in the basket | 1/5 (20.0%) | 0/5 (0%) | [BDDL](../task_review/definitions/Compose_009/task.bddl) · [Metadata](../task_review/definitions/Compose_009/task_meta.yaml) |
| COMPOSE_155 | Put the alphabet soup, the butter, and the tomato sauce in the basket one after another | 2/5 (40.0%) | 0/5 (0%) | [BDDL](../task_review/definitions/Compose_010/task.bddl) · [Metadata](../task_review/definitions/Compose_010/task_meta.yaml) |
| COMP2_027 | Put the cream cheese on the black bowl, and then push the plate to the front of the stove | 1/5 (20.0%) | 0/5 (0%) | [BDDL](../task_review/definitions/Compose_011/task.bddl) · [Metadata](../task_review/definitions/Compose_011/task_meta.yaml) |
| LBCM_003 | Put the tomato sauce in the basket, then put the white mug on the plate | 2/5 (40%) | 0/5 (0%) | [BDDL](../task_review/definitions/Compose_012/task.bddl) · [Metadata](../task_review/definitions/Compose_012/task_meta.yaml) |
| LBCM_028 | Put the alphabet soup in the basket, then put the white mug on the left plate, then put the cream cheese box in the basket | 1/5 (20%) | 0/5 (0%) | [BDDL](../task_review/definitions/Compose_013/task.bddl) · [Metadata](../task_review/definitions/Compose_013/task_meta.yaml) |
| MKDC_001 | Put the moka pot on the stove, then close the bottom drawer of the cabinet | 4/5 (80%) | 3/5 (60%) | [BDDL](../task_review/definitions/Compose_014/task.bddl) · [Metadata](../task_review/definitions/Compose_014/task_meta.yaml) |
| CTR_103 | Pick the butter and place it in the right compartment of the bowl drainer, then pick the tomato sauce and place it in the left compartment of the bowl drainer | 4/5 (80%) | Pending | [BDDL](../task_review/definitions/Compose_015/task.bddl) · [Metadata](../task_review/definitions/Compose_015/task_meta.yaml) |
| VCN35_004 | Put the ramekin in the basket, then put the alphabet soup on the right plate | 3/5 (60%) | 0/5 (0%) | [BDDL](../task_review/definitions/Compose_016/task.bddl) · [Metadata](../task_review/definitions/Compose_016/task_meta.yaml) |
| UCOMP_040 | Put the tomato sauce in the basket, and then put the yellow and white mug on the plate | 3/5 (60%) | 0/5 (0%) | [BDDL](../task_review/definitions/Compose_017/task.bddl) · [Metadata](../task_review/definitions/Compose_017/task_meta.yaml) |
| BDRMIN_002 | Pick the alphabet soup and place it in the right compartment of the bowl drainer, then pick the tomato sauce and place it in the left compartment of the bowl drainer | 1/5 (20%) | Pending | [BDDL](../task_review/definitions/Compose_018/task.bddl) · [Metadata](../task_review/definitions/Compose_018/task_meta.yaml) |
| CTR_176 | Put the alphabet soup in the basket, then put the butter in the basket, then put the cream cheese box in the basket | 5/5 (100%) | Pending | [BDDL](../task_review/definitions/Compose_019/task.bddl) · [Metadata](../task_review/definitions/Compose_019/task_meta.yaml) |
| CTR_140 | Put the cream cheese on the stove, then turn on the stove, then open the top drawer of the wooden cabinet | 1/5 (20%) | Pending | [BDDL](../task_review/definitions/Compose_020/task.bddl) · [Metadata](../task_review/definitions/Compose_020/task_meta.yaml) |

## TDL10_001 — provenance and evaluation

**Historical source note (status at its original recording date):**

**Current separate π0.5 result:** 0/5 (0%).

Skill sources: LIBERO_10_05. put the white mug on the left plate and put the yellow and white mug on the right plate

Scene construction: put the white mug on the left plate and put the yellow and white mug on the right plate

## TDL10_002 — provenance and evaluation

**Historical source note (status at its original recording date):**

**Current separate π0.5 result:** 0/5 (0%).

Skill sources: LIBERO_10_05. put the white mug on the left plate and put the yellow and white mug on the right plate

Scene construction: put the white mug on the left plate and put the yellow and white mug on the right plate

## TDL10_003 — provenance and evaluation

**Historical source note (status at its original recording date):**

**Current separate π0.5 result:** 0/5 (0%).

Skill sources: LIBERO_10_07. put the white mug on the plate and put the chocolate pudding to the right of the plate

Scene construction: put the white mug on the plate and put the chocolate pudding to the right of the plate

## TDL10_004 — provenance and evaluation

**Historical source note (status at its original recording date):**

**Current separate π0.5 result:** 0/5 (0%).

Skill sources: LIBERO_10_07. put the white mug on the plate and put the chocolate pudding to the right of the plate

Scene construction: put the white mug on the plate and put the chocolate pudding to the right of the plate

## TDL10_005 — provenance and evaluation

**Historical source note (status at its original recording date):**

**Current separate π0.5 result:** 0/5 (0%).

Skill sources: LIBERO_10_10. put the yellow and white mug in the microwave and close it

Scene construction: put the yellow and white mug in the microwave and close it

## TDL10_006 — provenance and evaluation

**Historical source note (status at its original recording date):**

**Current separate π0.5 result:** 1/5 (20%).

Skill sources: LIBERO_10_10. put the yellow and white mug in the microwave and close it

Scene construction: put the yellow and white mug in the microwave and close it

## TDL10_008 — provenance and evaluation

**Historical source note (status at its original recording date):**

**Current separate π0.5 result:** 0/5 (0%).

Skill sources: LIBERO_10_03. turn on the stove and put the moka pot on it

Scene construction: turn on the stove and put the moka pot on it

## TDL10_009 — provenance and evaluation

**Historical source note (status at its original recording date):**

**Current separate π0.5 result:** 0/5 (0%).

Skill sources: LIBERO_10_08. put both the alphabet soup and the cream cheese box in the basket

Scene construction: put both the alphabet soup and the cream cheese box in the basket

## TDL10_010 — provenance and evaluation

**Historical source note (status at its original recording date):**

**Current separate π0.5 result:** 0/5 (0%).

Skill sources: LIBERO_10_08. put both the alphabet soup and the cream cheese box in the basket

Scene construction: put both the alphabet soup and the cream cheese box in the basket

## TDL10_011 — provenance and evaluation

**Historical source note (status at its original recording date):**

**Current separate π0.5 result:** 0/5 (0%).

Skill sources: LIBERO_10_01. put both the alphabet soup and the tomato sauce in the basket

Scene construction: put both the alphabet soup and the tomato sauce in the basket

## TDL10_012 — provenance and evaluation

**Historical source note (status at its original recording date):**

**Current separate π0.5 result:** 0/5 (0%).

Skill sources: LIBERO_10_01. put both the alphabet soup and the tomato sauce in the basket

Scene construction: put both the alphabet soup and the tomato sauce in the basket

## TDL10_013 — provenance and evaluation

**Historical source note (status at its original recording date):**

**Current separate π0.5 result:** 0/5 (0%).

Skill sources: LIBERO_10_02. put both the cream cheese box and the butter in the basket

Scene construction: put both the cream cheese box and the butter in the basket

## TDL10_014 — provenance and evaluation

**Historical source note (status at its original recording date):**

**Current separate π0.5 result:** 0/5 (0%).

Skill sources: LIBERO_10_02. put both the cream cheese box and the butter in the basket

Scene construction: put both the cream cheese box and the butter in the basket

## TDL10_016 — provenance and evaluation

**Historical source note (status at its original recording date):**

**Current separate π0.5 result:** 0/5 (0%).

Skill sources: LIBERO_10_04. put the black bowl in the bottom drawer of the cabinet and close it

Scene construction: put the black bowl in the bottom drawer of the cabinet and close it

## TDC40_001 — provenance and evaluation

**Historical source note (status at its original recording date):**

**Current separate π0.5 result:** 0/5 (0%).

Skill sources: LIBERO_10_03. turn on the stove and put the moka pot on it

Scene construction: turn on the stove and put the moka pot on it

## TDC40_002 — provenance and evaluation

**Historical source note (status at its original recording date):**

**Current separate π0.5 result:** 0/5 (0%).

Skill sources: LIBERO_10_04. put the black bowl in the bottom drawer of the cabinet and close it

Scene construction: put the black bowl in the bottom drawer of the cabinet and close it

## TDC40_003 — provenance and evaluation

**Historical source note (status at its original recording date):**

**Current separate π0.5 result:** 2/5 (40%).

Skill sources: LIBERO_10_09. put both moka pots on the stove

Scene construction: put both moka pots on the stove

## TDC40_004 — provenance and evaluation

**Historical source note (status at its original recording date):**

**Current separate π0.5 result:** 0/5 (0%).

Skill sources: LIBERO_10_09. put both moka pots on the stove

Scene construction: put both moka pots on the stove

## TDC40_005 — provenance and evaluation

**Historical source note (status at its original recording date):**

**Current separate π0.5 result:** 0/5 (0%).

Skill sources: LIBERO_GOAL_04. Open the top layer of the drawer and put the bowl inside

Scene construction: Open the top layer of the drawer and put the bowl inside

## TDC40_006 — provenance and evaluation

**Historical source note (status at its original recording date):**

**Current separate π0.5 result:** 4/5 (80%).

Skill sources: LIBERO_GOAL_04. Open the top layer of the drawer and put the bowl inside

Scene construction: Open the top layer of the drawer and put the bowl inside

## ANLGX_002 — provenance and evaluation

**Historical source note (status at its original recording date):**

**Current separate π0.5 result:** 4/5 (80%).

Skill sources: LIBERO_10_05. put the white mug on the left plate and put the yellow and white mug on the right plate

Scene construction: put the white mug on the left plate and put the yellow and white mug on the right plate

## ANLGX_003 — provenance and evaluation

**Historical source note (status at its original recording date):**

**Current separate π0.5 result:** 0/5 (0%).

Skill sources: LIBERO_10_05. put the white mug on the left plate and put the yellow and white mug on the right plate

Scene construction: put the white mug on the left plate and put the yellow and white mug on the right plate

## ANLGX_017 — provenance and evaluation

**Historical source note (status at its original recording date):**

**Current separate π0.5 result:** 5/5 (100%).

Skill sources: LIBERO_10_04. put the black bowl in the bottom drawer of the cabinet and close it

Scene construction: put the black bowl in the bottom drawer of the cabinet and close it

## ANLGX_022 — provenance and evaluation

**Historical source note (status at its original recording date):**

**Current separate π0.5 result:** 0/5 (0%).

Skill sources: LIBERO_10_04. put the black bowl in the bottom drawer of the cabinet and close it

Scene construction: put the black bowl in the bottom drawer of the cabinet and close it

## ANLGX_023 — provenance and evaluation

**Historical source note (status at its original recording date):** ID clarification: ANLGX_023 closes the MIDDLE drawer (white_cabinet_1_middle_region); the selection shorthand said bottom. The explicitly selected ID is retained.

**Current separate π0.5 result:** 0/5 (0%).

Skill sources: LIBERO_10_04. put the black bowl in the bottom drawer of the cabinet and close it

Scene construction: put the black bowl in the bottom drawer of the cabinet and close it

## ANLGX_089 — provenance and evaluation

**Historical source note (status at its original recording date):** Recorded prompt is shown verbatim. Task-only rewrite for a future evaluation: Pick up the wine bottle and place it on the plate.

**Current separate π0.5 result:** 2/5 (40%).

Skill sources: LIBERO_SPATIAL_03. Pick the akita black bowl from table center and place it on the plate

Scene construction: Pick the akita black bowl from table center and place it on the plate

## ANLGX_134 — provenance and evaluation

**Historical source note (status at its original recording date):** The selected ANLGX run has one success video (1/5); the later ADAPT_007 run recorded 0/5. Both records are retained.

**Current separate π0.5 result:** 0/5 (0%).

Skill sources: LIBERO_GOAL_03. Put the wine bottle on the top of the drawer

Scene construction: Put the wine bottle on the top of the drawer

## ANLGX_147 — provenance and evaluation

**Historical source note (status at its original recording date):**

**Current separate π0.5 result:** 3/5 (60%).

Skill sources: LIBERO_GOAL_04. Open the top layer of the drawer and put the bowl inside

Scene construction: Open the top layer of the drawer and put the bowl inside

## ANLGX_178 — provenance and evaluation

**Historical source note (status at its original recording date):**

**Current separate π0.5 result:** 0/5 (0%).

Skill sources: LIBERO_10_06. pick up the book and place it in the back compartment of the caddy

Scene construction: pick up the book and place it in the back compartment of the caddy

## OGTS_001 — provenance and evaluation

**Historical source note (status at its original recording date):** The finalized 50-episode exact-GT evaluation is the primary record; the earlier five-episode result is retained below.

**Current separate π0.5 result:** 4/5 (80%).

Skill sources: LIBERO_OBJECT_01. Pick the alphabet soup and place it in the basket

Scene construction: Pick the alphabet soup and place it in the basket

## OGTS_010 — provenance and evaluation

**Historical source note (status at its original recording date):** The finalized 50-episode exact-GT evaluation is the primary record; the earlier five-episode result is retained below.

**Current separate π0.5 result:** 0/5 (0%).

Skill sources: LIBERO_OBJECT_10. Pick the orange juice and place it in the basket

Scene construction: Pick the orange juice and place it in the basket

## OGDTSL_011 — provenance and evaluation

**Historical source note (status at its original recording date):** Selected from the exhaustive Adapt Object evaluation. The original scene geometry, object positions, basket, and pruned init states remain unchanged.

**Current separate π0.5 result:** 5/5 (100%).

Skill sources: LIBERO_OBJECT_06. Pick the tomato sauce and place it in the basket

Scene construction: Pick the butter and place it in the basket

## OGDTSL_046 — provenance and evaluation

**Historical source note (status at its original recording date):** Selected from the exhaustive Adapt Object evaluation. The original scene geometry, object positions, basket, and pruned init states remain unchanged.

**Current separate π0.5 result:** 5/5 (100%).

Skill sources: LIBERO_OBJECT_08. Pick the milk and place it in the basket

Scene construction: Pick the tomato sauce and place it in the basket

## VCN8_008 — provenance and evaluation

**Historical source note (status at its original recording date):** 2-step user-accepted composition from Batch8DiverseGoalPlacements. Strict success requires the requested native predicates to rise in order and all final BDDL goals to hold, with no Compose final-TC threshold. This ID is explicitly listed in USER_REVIEW_DECISIONS.accepted_ids; all other unreviewed candidates are excluded. This replaces COMP2_001: both test the placement-to-middle-drawer-open pattern, and the retained VCN8_008 record is stronger (4/5 versus 2/5).

**Current separate π0.5 result:** 0/5 (0%).

Skill sources: put_the_cream_cheese_in_the_bowl;open_the_middle_drawer_of_the_cabinet. Put the cream cheese on the bowl | Open the middle layer of the drawer

Scene construction: put_the_cream_cheese_in_the_bowl;open_the_middle_drawer_of_the_cabinet

## VCN9_010 — provenance and evaluation

**Historical source note (status at its original recording date):** 2-step user-accepted composition from Batch9DependentPlacementControls. Strict success requires the requested native predicates to rise in order and all final BDDL goals to hold, with no Compose final-TC threshold. This ID is explicitly listed in USER_REVIEW_DECISIONS.accepted_ids; all other unreviewed candidates are excluded. The original five-episode result and all successful clips are retained without rerun or rescoring.

**Current separate π0.5 result:** 0/5 (0%).

Skill sources: put_the_bowl_on_the_stove;turn_on_the_stove. Put the bowl on the stove | Turn on the stove

Scene construction: put_the_bowl_on_the_stove;turn_on_the_stove

## VCN10_001 — provenance and evaluation

**Historical source note (status at its original recording date):** 2-step user-accepted composition from Batch10CrossSkillExactDonors6. Strict success requires the requested native predicates to rise in order and all final BDDL goals to hold, with no Compose final-TC threshold. This ID is explicitly listed in USER_REVIEW_DECISIONS.accepted_ids; all other unreviewed candidates are excluded. The original five-episode result and all successful clips are retained without rerun or rescoring.

**Current separate π0.5 result:** 0/5 (0%).

Skill sources: put_the_bowl_on_the_stove;pick_up_the_cream_cheese_and_place_it_in_the_basket;push_the_plate_to_the_front_of_the_stove. Put the bowl on the stove | Pick the cream cheese and place it in the basket | Push the plate to the front of the stove

Scene construction: put_the_bowl_on_the_stove;pick_up_the_cream_cheese_and_place_it_in_the_basket;push_the_plate_to_the_front_of_the_stove

## VCN19_020 — provenance and evaluation

**Historical source note (status at its original recording date):** 2-step user-accepted composition from Batch19FeedbackDrivenCompose20/benchmark. Strict success requires the requested native predicates to rise in order and all final BDDL goals to hold, with no Compose final-TC threshold. This ID is explicitly listed in USER_REVIEW_DECISIONS.accepted_ids; all other unreviewed candidates are excluded. The only successful episode was manually verified as a deliberate top-drawer open followed by the exact ramekin-to-plate placement; no sibling-drawer side effect was observed. The original five-episode result is retained without rerun or rescoring.

**Current separate π0.5 result:** 3/5 (60%).

Skill sources: LIBERO_GOAL_04; ANLGX_092. Open the top drawer of the cabinet and put the bowl inside; Pick up the ramekin on the cookies box and place it on the plate

Scene construction: Exact evaluated ANLGX_092 donor scene; native top drawer retained

## VCN21_001 — provenance and evaluation

**Historical source note (status at its original recording date):** 2-step user-accepted composition from MokaOneThenMicrowaveClose20260906/benchmark. Strict success requires the requested native predicates to rise in order and all final BDDL goals to hold, with no Compose final-TC threshold. This ID is explicitly listed in USER_REVIEW_DECISIONS.accepted_ids; all other unreviewed candidates are excluded. The audited v3 run is 4/5. All four success clips were manually verified as moka placement followed by deliberate microwave-door closure. The strict gate requires direct microdoorroot contact backed by an active MuJoCo constraint and positive normal force in the two-control-step close window, plus moka/door-sweep clearance at placement, close rising, and final success. The existing run is retained without rerun or rescoring.

**Current separate π0.5 result:** 4/5 (80%).

Skill sources: LIBERO_10_09; LIBERO_10_10. put both moka pots on the stove | put the yellow and white mug in the microwave and close it

Scene construction: Same-index robot-frame donor transfer; five-state physical screen 5/5

## COMP2_012 — provenance and evaluation

**Historical source note (status at its original recording date):**

**Current separate π0.5 result:** 0/5 (0%).

Skill sources: libero_object:307;306. Pick the butter and place it in the basket | Pick the tomato sauce and place it in the basket

Scene construction: Put the butter, the tomato sauce, and the ketchup in the basket one after another.

## COMP2_032 — provenance and evaluation

**Historical source note (status at its original recording date):**

**Current separate π0.5 result:** 0/5 (0%).

Skill sources: libero_goal:6;10. Push the plate to the front of the stove | Open the middle layer of the drawer

Scene construction: Put the black bowl on the plate, then push the plate to the front of the stove, and finally open the middle drawer of the cabinet.

## COMP2_222 — provenance and evaluation

**Historical source note (status at its original recording date):**

**Current separate π0.5 result:** 0/5 (0%).

Skill sources: libero_object:301;306. Pick the alphabet soup and place it in the basket | Pick the tomato sauce and place it in the basket

Scene construction: Put the alphabet soup, the salad dressing, and the tomato sauce in the basket one after another.

## COMP2_303 — provenance and evaluation

**Historical source note (status at its original recording date):**

**Current separate π0.5 result:** 0/5 (0%).

Skill sources: libero_object:308;302. Pick the milk and place it in the basket | Pick the cream cheese and place it in the basket

Scene construction: Put the milk, the cream cheese box, and the tomato sauce in the basket one after another.

## COMPOSE_155 — provenance and evaluation

**Historical source note (status at its original recording date):** Three-object composition from the evaluated milk-removed LIBERO-10 scene. The original definition and five-episode result are retained; no reevaluation was performed.

**Current separate π0.5 result:** 0/5 (0%).

Skill sources: LIBERO_10_01;LIBERO_OBJECT_01;LIBERO_OBJECT_07;LIBERO_OBJECT_06. put both the alphabet soup and the tomato sauce in the basket | Pick the alphabet soup and place it in the basket | Pick the butter and place it in the basket | Pick the tomato sauce and place it in the basket

Scene construction: put both the alphabet soup and the tomato sauce in the basket

## COMP2_027 — provenance and evaluation

**Historical source note (status at its original recording date):**

**Current separate π0.5 result:** 0/5 (0%).

Skill sources: libero_goal:4;6. Put the cream cheese on the bowl | Push the plate to the front of the stove

Scene construction: Put the cream cheese on the black bowl, then put the black bowl on the plate, and finally push the plate to the front of the stove.

## LBCM_003 — provenance and evaluation

**Historical source note (status at its original recording date):** 2-step composition. Exact original donor pickup and destination poses are retained; only colliding non-task distractors are removed. SR requires the specified native-goal event order and the final native goals. Only officially successful episodes are included; no reevaluation or rescoring.

**Current separate π0.5 result:** 0/5 (0%).

Skill sources: LIBERO_10_01;LIBERO_10_07. put both the alphabet soup and the tomato sauce in the basket | put the white mug on the plate and put the chocolate pudding to the right of the plate

Scene construction: put both the alphabet soup and the tomato sauce in the basket

## LBCM_028 — provenance and evaluation

**Historical source note (status at its original recording date):** 3-step composition. Exact original donor pickup and destination poses are retained; only colliding non-task distractors are removed. SR requires the specified native-goal event order and the final native goals. Only officially successful episodes are included; no reevaluation or rescoring.

**Current separate π0.5 result:** 0/5 (0%).

Skill sources: LIBERO_10_08;LIBERO_10_05. put both the alphabet soup and the cream cheese box in the basket | put the white mug on the left plate and put the yellow and white mug on the right plate

Scene construction: put both the alphabet soup and the cream cheese box in the basket

## NAFR3_001 — provenance and evaluation

**Historical source note (status at its original recording date):** Move the popcorn 4 cm back and arrange all four packages in a compact 2-by-2 cluster with clear grasping gaps; tomato sauce stays on popcorn's robot-left. Original LIBERO / previous V2 / corrected V3 masked comparison. Only the unchanged GPU6/7 V3 five-episode evaluation is used; the interrupted GPU5/6 attempt is excluded. Historical build metadata is frozen; completed SR is recorded here. No reevaluation.

**Current separate π0.5 result:** 2/5 (40%).

Skill sources: LIBERO_OBJECT_09. Pick the chocolate pudding and place it in the basket

Scene construction: Put the bowl on the top of the drawer

## NAFR3_002 — provenance and evaluation

**Historical source note (status at its original recording date):** Place the existing light-colored yellow book and black book side by side at the same robot-depth, with a clear gap; keep the black book outside the target-to-shelf route. Original LIBERO / previous V2 / corrected V3 masked comparison. Only the unchanged GPU6/7 V3 five-episode evaluation is used; the interrupted GPU5/6 attempt is excluded. The light-colored book is the native yellow_book asset, not a renamed white_book. Historical build metadata is frozen; completed SR is recorded here. No reevaluation.

**Current separate π0.5 result:** 5/5 (100%).

Skill sources: LIBERO_10_06; LIBERO_GOAL_05. pick up the book and place it in the back compartment of the caddy; Put the bowl on the top of the drawer

Scene construction: pick up the book and place it in the back compartment of the caddy

## MKDC_001 — provenance and evaluation

**Historical source note (status at its original recording date):** 2-step composition: moka pot onto stove, then bottom-drawer close. Original pot pickup/stove/cabinet root poses are retained; the drawer starts 7cm open for collision clearance and the inactive second pot is removed. Uses only the new five-episode rerun: each success stops exactly on final goal/order completion, without a final TC gate. Intermediate subtask switching remains TC>0.7 twice. The earlier long videos and the failed ep002 are not included.

**Current separate π0.5 result:** 3/5 (60%).

Skill sources: LIBERO_10_09; LIBERO_10_04. put both moka pots on the stove | put the black bowl in the bottom drawer of the cabinet and close it

Scene construction: Original moka/stove poses + original cabinet root pose

## DSET_001 — provenance and evaluation

**Historical source note (status at its original recording date):** The learned Spatial-suite pickup and flat-destination release trajectory is transferred from the plate to the exposed center of the dining-set mat. The learned table-center pickup pose and source layout are retained; the plate destination is replaced by the exposed center of the physical dining-set mat. Success uses the ordinary LIBERO On predicate plus dining-set parent contact; the unsafe native center_region is excluded. All five original GPU6 episodes succeeded. No reevaluation or rescoring.

**Current separate π0.5 result:** 5/5 (100%).

Skill sources: LIBERO_SPATIAL_03. Pick the akita black bowl from table center and place it on the plate

Scene construction: Pick the akita black bowl from table center and place it on the plate

## BDRSWAP_001 — provenance and evaluation

**Historical source note (status at its original recording date):** NATIVE IN FIRST-ENTRY SUCCESS ONLY: 5/5. Not a released or supported placement success rate; ending drainer contact is 0/5. Only alphabet soup / salad dressing XY positions changed. All five original videos are retained; no rerun or rescoring. The new selected task has no pi0.5 result.

**Current separate π0.5 result:** 5/5 (100%).

Skill sources: LIBERO_OBJECT_01. Pick the alphabet soup and place it in the basket

Scene construction: Original Object scene; exact BDRSIDE_002 five-state XY swap

## CTR_103 — provenance and evaluation

Fresh trajectory-guided repair of BDRCOMP_013, whose historical result was 0/5. Both food identities are directly trained in the original LIBERO-40; their basket-placement skills transfer to the two drainer compartments. The original completion rule is retained: each object must be released and supported by the drainer floor for five consecutive control steps, in the requested order. All four successes passed full video review. This run uses the existing RAIN action and progress checkpoints. Policy seeds 7–11 differ from the parent, so the comparison does not isolate the effect of the pose change. User selected on 2026-09-11; frozen RAIN results reused without rerun. Separate pi0.5 evaluation pending.

Skill sources: LIBERO_OBJECT_06; LIBERO_OBJECT_07. Pick the tomato sauce and place it in the basket | Pick the butter and place it in the basket

Scene construction: BDRCOMP_013; butter/tomato original Object skills transferred to the drainer. Tomato XY shifts -4.5 cm, +7 cm. Parent and repaired policy seeds differ.

Ordered native left then right compartments; each object released with positive exact drainer-bottom support for five consecutive controls, with both placements retained. No velocity-settling claim. No final TC gate.

[Selection provenance](CTR_103_PROVENANCE.json)

## ADVCN19_001 — provenance and evaluation

**Historical source note (status at its original recording date):** Atomic Adapt: only open the top drawer. The five initial states, all objects, positions and fixture poses are exactly preserved from VCN19_020; ramekin placement is removed from the instruction, goal and action plan. Native Open starts false and is the sole success condition. The interaction mask covers the moving top drawer only, not the whole cabinet or sibling drawers. The complete altered Spatial scene is not claimed to have appeared in training. A separate strict π0.5 five-episode evaluation is now published: 4/5 under the atomic Open rule.

**Current separate π0.5 result:** 4/5 (80%).

Skill sources: LIBERO_GOAL_04. Open the top drawer and put the bowl inside. (Opening action only.)

Scene construction: Open the top drawer of the wooden cabinet, then put the ramekin on the plate.

## WTRAYR_004 — provenance and evaluation

**Historical source note (status at its original recording date):** Selected reachable-pose wooden-tray Adapt. The tray is shifted 6 cm to robot-right and the black-bowl pickup is shifted 3 cm toward the robot and 5 cm toward the center relative to WTRAY_004. Historical RAIN success is strict 2/5 (episodes 1 and 2): native In, the complete collision envelope inside the native tray site with 1 mm tolerance, positive-force tray contact, no gripper contact, and all conditions held for five consecutive control steps. WTRAYR_004 now has an independent strict π0.5 result of 5/5 (100%). Its historical RAIN result is unchanged.

**Current separate π0.5 result:** 5/5 (100%).

Skill sources: LIBERO_SPATIAL_03. Pick the akita black bowl from table center and place it on the plate

Scene construction: Pick up the black bowl and place it in the wooden tray.

## GRACK_002 — provenance and evaluation

**Historical source note (status at its original recording date):** Only the original Goal10 wine identity is replaced by the native ketchup asset at the exact original wine pickup XY; all other scene objects, fixtures and rack orientation are preserved. Historical RAIN is strict 5/5: the actual upper-deck annotated On region, root above its footprint, positive upper-deck support force, no gripper contact and a five-control-step hold. The original wine-specific native On is auxiliary only (0/5 final and ever), not this Adapt success metric. The evaluated whole-rack GT mask contains observed stray stove pixels; this limitation is preserved, not silently corrected. GRACK_002 now has an independent strict π0.5 result of 4/5 (80%). Its historical RAIN result is unchanged.

**Current separate π0.5 result:** 4/5 (80%).

Skill sources: LIBERO_GOAL_10; LIBERO_OBJECT_05. Put the wine bottle on the rack; Pick up the ketchup and place it in the basket

Scene construction: Put the wine bottle on the rack

## VCN35_004 — provenance and evaluation

**Historical source note (status at its original recording date):** Two-step user-selected composition. The ramekin pickup, basket target, alphabet-soup pickup, and right-plate target retain evaluated same-index robot-frame donor transforms; there is no manual coordinate offset or height repair. Strict success requires both native predicates to rise in the requested order, both final BDDL goals to hold, and the ramekin placement to remain intact through the later soup placement. Compose final completion has no TC threshold. Original episodes 001, 002, and 004 passed manual video review. The frozen 3/5 result is reused without rerun or rescoring. A separate π0.5 five-episode evaluation is now complete: 0/5 (0%). The historical RAIN record is unchanged.

**Current separate π0.5 result:** 0/5 (0%).

Skill sources: WTRAYR_005; LBCM_003; ADAPT_088. Pick up the ramekin and place it in the wooden tray | Put the tomato sauce in the basket, then put the white mug on the plate | Put the alphabet soup on the right front plate

Scene construction: Exact evaluated cylinder/right-plate and tabletop basket target transforms

## UCOMP_040 — provenance and evaluation

**Historical source note (status at its original recording date):** Two-step user-selected composition. Tomato sauce is placed in the basket first, followed by the yellow-and-white mug on the plate. The evaluated task keeps source-aligned pickup and destination slots. Strict success requires both native predicates to rise in the requested order, both final BDDL goals to hold, and the first relation to survive the second action. Compose final completion has no TC threshold. Episodes 000, 001, and 002 passed the campaign-wide manual success-video review. The frozen 3/5 result is reused without rerun or rescoring; A separate π0.5 five-episode evaluation is now complete: 0/5 (0%). The historical RAIN record is unchanged.

**Current separate π0.5 result:** 0/5 (0%).

Skill sources: LIBERO_OBJECT_06; LIBERO_10_05. Pick the tomato sauce and place it in the basket | Put the white mug on the left plate and put the yellow and white mug on the right plate

Scene construction: Source-aligned Object-05 pickup/basket geometry with the evaluated yellow-mug/plate slot

## BDRMIN_002 — provenance and evaluation

**Historical source note (status at its original recording date):** User-selected reverse-order bowl-drainer Compose result. Strict RAIN success is 1/5 (episode 004): alphabet soup completes the right placement before tomato sauce completes the left placement. Both selected native In predicates are true at termination, neither opposite compartment is entered, and both objects are released with exact bottom support held for five consecutive control steps. The first placement remains supported through the second. Final termination has no TC threshold. The frozen five-episode result is reused without rerun or rescoring; a separate pi0.5 evaluation is pending.

**Current separate π0.5 result:** Pending.

Skill sources: LIBERO_OBJECT_01; LIBERO_OBJECT_06. Pick the alphabet soup and place it in the basket | Pick the tomato sauce and place it in the basket

Scene construction: Each object retains its original LIBERO-Object target pickup-slot family; non-interacting distractors are removed.

## CTR_176 — provenance and evaluation

Soup -> butter -> cream cheese into the basket:5/5 fully reviewed released/supported/settled successes. The underlying scene repair CTR_163 moves cheese12.5cm in negativeX and14.5cm in positiveY toward historical COMPOSE_152 failed closing trajectories; the original COMPOSE_152 was0/5. This CTR_176 followup retains CTR_163 geometry and seeds unchanged and applies the already declared stricter physical terminal protocol. ParentCTR_163 native5/5 is preserved; it terminates earlier at the last native In event and is not a settled-placement5/5 certificate. Across all five episodes every saved policy action and state matches the parent bitwise through its cutoff, then the same release policy runs6-16 more controls inside the unchanged1200 cap. This is one existing three-food composition and a protocol followup, not an additional new scene or proof of population-level100% reliability. User selected on 2026-09-11; frozen RAIN results reused without rerun. Separate pi0.5 evaluation pending.

Skill sources: LIBERO_OBJECT_01; LIBERO_OBJECT_07; LIBERO_OBJECT_02. Pick the alphabet soup and place it in the basket | Pick the butter and place it in the basket | Pick the cream cheese and place it in the basket

Scene construction: COMPOSE_152 via CTR_163; LIBERO10-derived scene and three original Object basket skills. Cheese XY shifts -12.5 cm, +14.5 cm from COMPOSE_152. CTR_176 retains CTR_163 geometry and seeds.

Ordered basket goals plus released/supported/settled completion for five consecutive controls; positive support paths to the exact basket base, no robot contact, linear speed <= 0.02 m/s and angular speed <= 0.5 rad/s. Same 1200-control cap and no final TC gate.

[Selection provenance](CTR_176_PROVENANCE.json)

## CTR_140 — provenance and evaluation

Three-step repair of historical VCN16_001 (0/5): place cheese on the stove, turn on that stove, then open the wooden top drawer. The entire stove moves10cm in positive worldX toward the observed missed-knob approach, carrying its burner and knob together. This also changes the first placement target. Cheese, cabinet, action plan and native ordered goals retain their parent definitions. All five frozen states pass physical validation; the fresh existing-RAIN run completes1/5 with a full video/trace certificate. The first placement includes a documented transfer of the trained bowl-to-stove destination to directly trained cream-cheese grasping. This is an exploratory repaired composition; the five-trial result is not a general success-rate claim. User selected on 2026-09-11; frozen RAIN results reused without rerun. Separate pi0.5 evaluation pending.

Skill sources: LIBERO_OBJECT_02; LIBERO_GOAL_02; LIBERO_GOAL_08; LIBERO_GOAL_04. Pick the cream cheese and place it in the basket | Put the bowl on the stove | Turn on the stove | Open the top layer of the drawer and put the bowl inside

Scene construction: VCN16_001; Object cheese grasp + Goal stove placement, stove ON, top-drawer opening. Entire stove shifts +10 cm world X, including burner and knob.

Ordered cheese-on-stove, stove ON, then top-drawer Open; all final BDDL goals hold. Stove inference uses the exact knob mask. No final TC gate.

[Selection provenance](CTR_140_PROVENANCE.json)
