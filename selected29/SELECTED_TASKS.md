# Selected LIBERO-EX tasks

Selection updated 2026-09-06. 20 Decomposition + 17 Adapt + 14 Compose (51 total). The confirmed Compose IDs are VCN8_008, VCN9_010, VCN10_001, VCN19_020, COMP2_012, COMP2_032, COMP2_222, COMP2_303, COMPOSE_155, COMP2_027, LBCM_003, LBCM_028, MKDC_001, BDRCOMP_021.

A separate π0.5 evaluation was previously run with the official `pi05_libero` checkpoint fine-tuned on LIBERO-40. Of the current selection, 47/51 tasks retain exactly 5 evaluated episodes (235 total), with 58 successful episodes (24.7%) and 16/47 evaluated tasks succeeding at least once. VCN8_008, VCN9_010, VCN10_001, VCN19_020 were selected after that run and are explicitly marked not evaluated; no π0.5 result is inferred from their RAIN records. COMP2_001's old π0.5 record remains frozen in the source ledger but is retired from this page. See [`pi05_results.tsv`](pi05_results.tsv), [`pi05_episodes.tsv`](pi05_episodes.tsv), and [`pi05_evaluation.json`](pi05_evaluation.json).

Adapt retains the selected task definitions and evaluation records. ADAPT_001–009 are task-definition matches for the nine ANLGX tasks and have separate five-episode reruns. OGTS_001 and OGTS_010 use their finalized exact-GT 50-episode evaluations as primary, while retaining their earlier 4/5 results as additional records. OGDTSL_011 and OGDTSL_046 retain their original Adapt Object five-episode evaluations. Historical metadata may still call some sources Analogy or Object; the collection category is Adapt.

Selected Analogy/Adapt now also includes NAFR3_001 and NAFR3_002, each 4/5 (80%) on GPUs 6/7. Each retains all four original successful episodes and the original LIBERO / V2 / V3 masked comparison. The light-colored book remains the native yellow_book asset. No V1/V2 results or interrupted GPU5/6 episodes are mixed in. The standalone NAF revisions public page is retired; its experimental source records and offline review archive remain preserved.

DSET_001 is selected as Adapt using its unchanged 5/5 (100%) GPU6 evaluation. The black bowl retains the learned LIBERO_SPATIAL_03 table-center pickup pose, while the plate destination is replaced by the exposed center of the physical dining-set mat. The Selected page retains all five original successful episodes, the masked comparison, and a self-contained task bundle after the standalone dining-set review page is retired.

BDRSWAP_001 is selected as Adapt with its frozen native `In` 5/5 record; that historical metric is first entry into the exact right compartment and is not a released/support claim. Its separate π0.5 run uses the same native goal. BDRCOMP_021 is selected as Compose with its frozen strict 2/5 record and is also scored strictly for π0.5: left then right, exact native compartment `In`, gripper released, positive bottom-support force held for five consecutive control steps, with both placements retained at termination.

Compose retains each selected Composition2Step, Compose-350, Long Basket/Cup Mix, MKDC, bowl-drainer, or accepted VCN task definition, five-episode RAIN evaluation, masked comparison and saved success videos. The user's COM2_027 shorthand was explicitly confirmed to mean COMP2_027.

COMP2_001 is removed and replaced by VCN8_008 because both exercise the same placement→middle-drawer-open pattern, while VCN8_008 has the stronger RAIN result: 4/5 (80%) rather than 2/5 (40%). User-accepted VCN9_010 is added at 4/5 (80%), VCN10_001 at 2/5 (40%), and VCN19_020 at 1/5 (20%). VCN19_020 ep000 was manually verified as a deliberate top-drawer open followed by ramekin-to-plate placement. Only IDs in `USER_REVIEW_DECISIONS.accepted_ids` are included; every other Batch19 candidate remains excluded.

MKDC_001 is added as Compose using its historical RAIN goal/order-stop five-episode rerun: 4/5 (80%), saved successful episodes 000, 001, 003, 004. Every RAIN success stops exactly on the final goal step, without TC gating final termination; intermediate subtask switching remains TC>0.7 twice. The original pot/stove/cabinet root poses are preserved; the bottom drawer starts 7cm open for clearance and the inactive second moka pot is removed. The earlier long videos and failed ep002 are excluded from that historical record. The new π0.5 result is reported only in its separate column.

ANLGX_023 is **middle drawer close**, not bottom drawer close. Selection follows the explicit ID. ANLGX_178 is **yellow-and-white mug to the left compartment of the caddy**.

ANLGX_089 preserves the evaluated instruction. Its task-only wording for a future evaluation is `Pick up the wine bottle and place it on the plate.`; its historical SR is not a result for that revised prompt.

## Decomposition

| Task ID | Alias | Recorded instruction | Historical RAIN SR | π0.5 LIBERO-40 SR (5ep) | Additional historical SR |
|---|---|---|---|---|---|
| TDL10_001 | DECOMP_001 | Put the white mug on the left plate. | 33/50 (66.0%) | 0/5 (0%) | — |
| TDL10_002 | DECOMP_002 | Put the yellow and white mug on the right plate. | 50/50 (100.0%) | 0/5 (0%) | — |
| TDL10_003 | DECOMP_003 | Put the white mug on the plate. | 14/50 (28.0%) | 0/5 (0%) | — |
| TDL10_004 | DECOMP_004 | Put the chocolate pudding to the right of the plate. | 49/50 (98.0%) | 0/5 (0%) | — |
| TDL10_005 | DECOMP_005 | Put the yellow and white mug in the microwave. | 20/50 (40.0%) | 0/5 (0%) | — |
| TDL10_006 | DECOMP_006 | Close the microwave. | 47/50 (94.0%) | 1/5 (20%) | — |
| TDL10_008 | DECOMP_007 | Put the moka pot on the stove. | 10/50 (20.0%) | 0/5 (0%) | — |
| TDL10_009 | DECOMP_008 | Put the alphabet soup in the basket. | 50/50 (100.0%) | 0/5 (0%) | — |
| TDL10_010 | DECOMP_009 | Put the cream cheese box in the basket. | 41/50 (82.0%) | 0/5 (0%) | — |
| TDL10_011 | DECOMP_010 | Put the alphabet soup in the basket. | 45/50 (90.0%) | 0/5 (0%) | — |
| TDL10_012 | DECOMP_011 | Put the tomato sauce in the basket. | 48/50 (96.0%) | 0/5 (0%) | — |
| TDL10_013 | DECOMP_012 | Put the cream cheese box in the basket. | 22/50 (44.0%) | 0/5 (0%) | — |
| TDL10_014 | DECOMP_013 | Put the butter in the basket. | 50/50 (100.0%) | 0/5 (0%) | — |
| TDL10_016 | DECOMP_014 | Close the bottom drawer of the cabinet. | 16/50 (32.0%) | 0/5 (0%) | — |
| TDC40_001 | DECOMP_015 | Turn on the stove. | 2/10 (20.0%) | 0/5 (0%) | — |
| TDC40_002 | DECOMP_016 | Put the black bowl in the bottom drawer of the cabinet. | 0/10 (0.0%) | 0/5 (0%) | — |
| TDC40_003 | DECOMP_017 | Put the left moka pot on the stove. | 9/10 (90.0%) | 2/5 (40%) | — |
| TDC40_004 | DECOMP_018 | Put the right moka pot on the stove. | 0/10 (0.0%) | 0/5 (0%) | — |
| TDC40_005 | DECOMP_019 | Open the top drawer of the cabinet. | 1/10 (10.0%) | 0/5 (0%) | — |
| TDC40_006 | DECOMP_020 | Put the black bowl inside the top drawer of the cabinet. | 10/10 (100.0%) | 4/5 (80%) | — |

## Adapt

| Task ID | Alias | Recorded instruction | Historical RAIN SR | π0.5 LIBERO-40 SR (5ep) | Additional historical SR |
|---|---|---|---|---|---|
| ANLGX_002 | ADAPT_001 | Put the white mug on the middle plate. | 4/5 (80.0%) | 4/5 (80%) | Later ADAPT_001: 3/5 (60.0%) |
| ANLGX_003 | ADAPT_002 | Put the white mug on the right plate. | 3/5 (60.0%) | 0/5 (0%) | Later ADAPT_002: 3/5 (60.0%) |
| ANLGX_017 | ADAPT_003 | Put the black bowl in the middle drawer of the white cabinet. | 5/5 (100.0%) | 5/5 (100%) | Later ADAPT_003: 5/5 (100.0%) |
| ANLGX_022 | ADAPT_004 | Close the top drawer of the white cabinet. | 4/5 (80.0%) | 0/5 (0%) | Later ADAPT_004: 3/5 (60.0%) |
| ANLGX_023 | ADAPT_005 | Close the middle drawer of the white cabinet. | 4/5 (80.0%) | 3/5 (60%) | Later ADAPT_005: 5/5 (100.0%) |
| ANLGX_089 | ADAPT_006 | Pick up the wine bottle at the table center and place it on the plate. | 3/5 (60.0%) | 2/5 (40%) | Later ADAPT_006: 3/5 (60.0%) |
| ANLGX_134 | ADAPT_007 | Put the plate on the top of the wooden cabinet. | 1/5 (20.0%) | 0/5 (0%) | Later ADAPT_007: 0/5 (0.0%) |
| ANLGX_147 | ADAPT_008 | Put the cream cheese in the top drawer of the wooden cabinet. | 3/5 (60.0%) | 3/5 (60%) | Later ADAPT_008: 3/5 (60.0%) |
| ANLGX_178 | ADAPT_009 | Put the yellow and white mug in the left compartment of the caddy. | 3/5 (60.0%) | 0/5 (0%) | Later ADAPT_009: 1/5 (20.0%) |
| OGTS_001 | OGTS_001 | Pick the alphabet soup and place it in the basket | 48/50 (96.0%) | 4/5 (80%) | Earlier PositionSwap 5ep: 4/5 (80.0%) |
| OGTS_010 | OGTS_010 | Pick the orange juice and place it in the basket | 26/50 (52.0%) | 0/5 (0%) | Earlier PositionSwap 5ep: 4/5 (80.0%) |
| OGDTSL_011 | OGDTSL_011 | Pick the tomato sauce and place it in the basket | 4/5 (80.0%) | 5/5 (100%) | — |
| OGDTSL_046 | OGDTSL_046 | Pick the milk and place it in the basket | 2/5 (40.0%) | 5/5 (100%) | — |
| NAFR3_001 | NAFR3_001 | Put the popcorn on top of the short fridge. | 4/5 (80%) | 2/5 (40%) | — |
| NAFR3_002 | NAFR3_002 | Put the yellow book on top of the two-layer wooden shelf. | 4/5 (80%) | 5/5 (100%) | — |
| DSET_001 | DSET_001 | Pick up the black bowl at the table center and place it on the dining-set mat. | 5/5 (100.0%) | 5/5 (100%) | — |
| BDRSWAP_001 | BDRSWAP_001 | Pick the alphabet soup and place it in the right compartment of the bowl drainer. | 5/5 (100%) | 5/5 (100%) | — |

## Compose

| Task ID | Alias | Recorded instruction | Historical RAIN SR | π0.5 LIBERO-40 SR (5ep) | Additional historical SR |
|---|---|---|---|---|---|
| VCN8_008 | VCN8_008 | Put the chocolate pudding on the black bowl, then open the middle drawer of the cabinet. | 4/5 (80%) | Not evaluated | — |
| VCN9_010 | VCN9_010 | Put the cream cheese on the stove, then turn on the stove. | 4/5 (80%) | Not evaluated | — |
| VCN10_001 | VCN10_001 | Put the cream cheese on the stove, then push the plate to the front of the stove. | 2/5 (40%) | Not evaluated | — |
| VCN19_020 | VCN19_020 | Open the top drawer of the wooden cabinet, then put the ramekin on the plate. | 1/5 (20%) | Not evaluated | — |
| COMP2_012 | COMP2_012 | Put the butter in the basket, and then put the tomato sauce in the basket. | 5/5 (100.0%) | 0/5 (0%) | — |
| COMP2_032 | COMP2_032 | Push the plate to the front of the stove, and then open the middle drawer of the cabinet. | 1/5 (20.0%) | 0/5 (0%) | — |
| COMP2_222 | COMP2_222 | Put the alphabet soup in the basket, and then put the tomato sauce in the basket. | 1/5 (20.0%) | 0/5 (0%) | — |
| COMP2_303 | COMP2_303 | Put the milk in the basket, and then put the cream cheese box in the basket. | 1/5 (20.0%) | 0/5 (0%) | — |
| COMPOSE_155 | COMPOSE_155 | Put the alphabet soup, the butter, and the tomato sauce in the basket one after another. | 2/5 (40.0%) | 0/5 (0%) | — |
| COMP2_027 | COMP2_027 | Put the cream cheese on the black bowl, and then push the plate to the front of the stove. | 1/5 (20.0%) | 0/5 (0%) | — |
| LBCM_003 | LBCM_003 | Put the tomato sauce in the basket, then put the white mug on the plate. | 2/5 (40%) | 0/5 (0%) | — |
| LBCM_028 | LBCM_028 | Put the alphabet soup in the basket, then put the white mug on the left plate, then put the cream cheese box in the basket. | 1/5 (20%) | 0/5 (0%) | — |
| MKDC_001 | MKDC_001 | Put the moka pot on the stove, then close the bottom drawer of the cabinet. | 4/5 (80%) | 3/5 (60%) | — |
| BDRCOMP_021 | BDRCOMP_021 | Pick the alphabet soup and place it in the left compartment of the bowl drainer, then pick the salad dressing and place it in the right compartment of the bowl drainer. | 2/5 (40%) | 0/5 (0%) | — |
