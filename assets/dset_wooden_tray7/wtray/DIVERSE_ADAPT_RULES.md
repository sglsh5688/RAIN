# Wooden tray · three-object choice tasks

## Scene and exact success rule

All six tasks use the living-room table and the unscaled native `wooden_tray` asset. The tray center is `(x,y)=(+0.10,0.00)` with authored range `x=[0.099,0.101]`, `y=[-0.001,0.001]`, yaw `0`.

The three visible choices share `x=-0.13` (`[-0.133,-0.127]`): left is `y=-0.23` (`[-0.233,-0.227]`), middle is `y=0` (`[-0.003,0.003]`), and right is `y=+0.23` (`[0.227,0.233]`). All start on the table and outside the tray.

Each task has one native `In(selected_object, wooden_tray_1_contain_region)` goal. Reported success additionally requires the selected object's full collision envelope inside the native site (1 mm tolerance), positive-force contact with the tray, no gripper contact, and five consecutive supported control steps. Distractors have no terminal condition. The episode limit is 520 control steps.

## RAIN five-episode result

The completed run contains 30 unique episodes on physical GPUs 6/7 using base seed 7 and deterministic per-task/per-episode derived seeds: **2/30 strict successes**. Only `WTRAY_004` succeeded (`2/5`, episodes 2 and 4); strict contact began at control steps 329/462 and completed the five-step hold at 333/466. All 30 initial goals were false. All 30 original outcome videos are retained and hash-verified.

| ID | Selected choice and position | Full instruction | Exact goal | Source/position context | GPU | Result |
|---|---|---|---|---|---:|---:|
| `WTRAY_001` | `plate_1`, left (-0.13,-0.23) | Pick up the left plate and place it in the wooden tray. | `in(plate_1, wooden_tray_1_contain_region)` | LIBERO_10_05 plates were at (0,-0.30)/(0,+0.30); selects new left plate. | 6 | **0/5** |
| `WTRAY_002` | `plate_2`, middle (-0.13,0.00) | Pick up the middle plate and place it in the wooden tray. | `in(plate_2, wooden_tray_1_contain_region)` | LIBERO_10_05 + added midpoint choice; selects middle plate. | 7 | **0/5** |
| `WTRAY_003` | `plate_3`, right (-0.13,+0.23) | Pick up the right plate and place it in the wooden tray. | `in(plate_3, wooden_tray_1_contain_region)` | LIBERO_10_05 plates were at (0,-0.30)/(0,+0.30); selects new right plate. | 6 | **0/5** |
| `WTRAY_004` | `akita_black_bowl_1`, left (-0.13,-0.23) | Pick up the black bowl and place it in the wooden tray. | `in(akita_black_bowl_1, wooden_tray_1_contain_region)` | LIBERO_SPATIAL_03 black bowl center (-0.075,0), plate target (+0.06,+0.20). | 7 | **2/5** |
| `WTRAY_005` | `glazed_rim_porcelain_ramekin_1`, middle (-0.13,0.00) | Pick up the ramekin and place it in the wooden tray. | `in(glazed_rim_porcelain_ramekin_1, wooden_tray_1_contain_region)` | LIBERO_SPATIAL_03 initialization (original ramekin center -0.20,+0.20); evidence ANLGX_088/DSET_004. | 6 | **0/5** |
| `WTRAY_006` | `white_bowl_1`, right (-0.13,+0.23) | Pick up the white bowl and place it in the wooden tray. | `in(white_bowl_1, wooden_tray_1_contain_region)` | LIBERO_SPATIAL_03 initialization; DSET_005 white-bowl pickup center (-0.075,0). | 7 | **0/5** |

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
