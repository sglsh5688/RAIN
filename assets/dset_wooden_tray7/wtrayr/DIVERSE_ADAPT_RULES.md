# Reachable wooden-tray object-choice revisions

## Controlled geometry revision

These six tasks are direct revisions of `WTRAY_001..006`. The native, unscaled `wooden_tray` is translated 6 cm toward robot-right: `(x,y)=(+0.10,0.00)` → `(+0.10,-0.06)`, with yaw, mesh, collision geometry, and native `contain_region` unchanged.

Plate positions are unchanged. In the heterogeneous scene only, the black-bowl pickup center is changed from `(-0.13,-0.23)` to `(-0.16,-0.18)`; the ramekin and white-bowl positions are unchanged. Every task retains three visible choices, one exact selected-object mask, and one current native-tray-site mask. Stored and union masks are forbidden.

## Exact success rule

Each task has one native `In(selected_object, wooden_tray_1_contain_region)` goal. Reported success additionally requires the selected object's full collision envelope inside the native site (1 mm tolerance), positive-force tray contact, no gripper contact, and five consecutive supported control steps. Native root-only `In` is auxiliary. The episode limit is 520 control steps.

## RAIN five-episode result

The completed run contains 30 unique episodes on physical GPUs 6/7 with base seed 7: **5/30 strict successes (16.7%)**. Successful trials: `WTRAYR_004` episodes 1, 2; `WTRAYR_005` episodes 2; `WTRAYR_006` episodes 0, 2. All 30 initial goals were false, and all 30 original outcome videos are retained, decoded, and hash-verified.

Strict success witnesses: `WTRAYR_004` ep1: strict onset 243, hold complete 247; `WTRAYR_004` ep2: strict onset 259, hold complete 263; `WTRAYR_005` ep2: strict onset 129, hold complete 133; `WTRAYR_006` ep0: strict onset 202, hold complete 206; `WTRAYR_006` ep2: strict onset 354, hold complete 358.

| ID | Predecessor | Selected choice and position | Full instruction | Exact goal | GPU | Result |
|---|---|---|---|---|---:|---:|
| `WTRAYR_001` | `WTRAY_001` | `plate_1`, left `(-0.13,-0.23)` | Pick up the left plate and place it in the wooden tray. | `in(plate_1, wooden_tray_1_contain_region)` | 6 | **0/5** |
| `WTRAYR_002` | `WTRAY_002` | `plate_2`, middle `(-0.13,0.00)` | Pick up the middle plate and place it in the wooden tray. | `in(plate_2, wooden_tray_1_contain_region)` | 7 | **0/5** |
| `WTRAYR_003` | `WTRAY_003` | `plate_3`, right `(-0.13,+0.23)` | Pick up the right plate and place it in the wooden tray. | `in(plate_3, wooden_tray_1_contain_region)` | 6 | **0/5** |
| `WTRAYR_004` | `WTRAY_004` | `akita_black_bowl_1`, revised `(-0.16,-0.18)` | Pick up the black bowl and place it in the wooden tray. | `in(akita_black_bowl_1, wooden_tray_1_contain_region)` | 7 | **2/5** |
| `WTRAYR_005` | `WTRAY_005` | `glazed_rim_porcelain_ramekin_1`, middle `(-0.13,0.00)` | Pick up the ramekin and place it in the wooden tray. | `in(glazed_rim_porcelain_ramekin_1, wooden_tray_1_contain_region)` | 6 | **1/5** |
| `WTRAYR_006` | `WTRAY_006` | `white_bowl_1`, right `(-0.13,+0.23)` | Pick up the white bowl and place it in the wooden tray. | `in(white_bowl_1, wooden_tray_1_contain_region)` | 7 | **2/5** |

## Result artifacts

- [Per-task success rates](evaluation_5ep/task_success_rates.tsv)
- [Episode outcomes](evaluation_5ep/episodes.tsv)
- [Success-video ledger](evaluation_5ep/success_videos.tsv)
- [Failure-video ledger](evaluation_5ep/failure_videos.tsv)
- [Evaluation summary](evaluation_5ep/SUMMARY.md)
- [Post-evaluation run manifest](evaluation_5ep/run_manifest.json)
- [Post-evaluation audit](evaluation_5ep/AUDIT.json)
- [SHA-256 ledger](evaluation_5ep/POST_EVAL_SHA256.tsv)

No GitHub upload was performed.
