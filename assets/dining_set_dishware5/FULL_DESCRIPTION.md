# Dining-set dishware tasks · full description and results

## Shared construction

- Source scene family: original LIBERO-Spatial layouts.
- Destination substitution: replace the source `plate_1` with `dining_set_group_1` at the exact same table center `(0.06, 0.20)` and yaw.
- Documented blocker removal: remove only `akita_black_bowl_2`, whose original `(0.01, 0.31)` pose overlaps the much wider dining-set footprint. The table, wooden cabinet, flat stove, cookies, and other nonblocking context remain.
- Target: `dining_set_group_1_plate_support_region`, the exposed central cloth between the utensil groups.
- Excluded target: the asset's native `center_region`, because it lies below the real collision support surface.
- Success predicate: ordinary LIBERO `On(manipulated_object, dining_set_group_1_plate_support_region)`. The object root must be above the finite site and the object must physically contact the dining-set parent.
- Policy masks: exact current-simulator instance mask for the manipulated object and exact current projection of the target site; no stored target mask fallback.
- Initialization: five distinct, settled states per task; every initial goal is false and both required masks are visible.
- Evaluation: five original policy episodes per task, physical GPUs 6 and 7, unchanged RAIN multi-scale mask-augmentation checkpoints, 520-step budget.

## Task definitions

### DSET_001

- Full instruction: **Pick up the black bowl at the table center and place it on the dining-set mat.**
- Source: `LIBERO_SPATIAL_03`.
- Manipulated object: `akita_black_bowl_1` (`akita_black_bowl`).
- Initial relation: `On(akita_black_bowl_1, main_table_table_center)`.
- Goal: `On(akita_black_bowl_1, dining_set_group_1_plate_support_region)`.
- Transfer rationale: preserves the learned table-center black-bowl pickup and flat tableware release trajectory.
- Result: **5/5 (100%)**.

### DSET_002

- Full instruction: **Pick up the black bowl on the cookies box and place it on the dining-set mat.**
- Source: `LIBERO_SPATIAL_04`.
- Manipulated object: `akita_black_bowl_1` (`akita_black_bowl`).
- Initial relation: `On(akita_black_bowl_1, cookies_1)`.
- Goal: `On(akita_black_bowl_1, dining_set_group_1_plate_support_region)`.
- Transfer rationale: preserves the learned pickup from the cookies-box support and changes only the plate destination.
- Result: **5/5 (100%)**.

### DSET_003

- Full instruction: **Pick up the black bowl on top of the wooden cabinet and place it on the dining-set mat.**
- Source: `LIBERO_SPATIAL_10`.
- Manipulated object: `akita_black_bowl_1` (`akita_black_bowl`).
- Initial relation: `On(akita_black_bowl_1, wooden_cabinet_1_top_side)`.
- Goal: `On(akita_black_bowl_1, dining_set_group_1_plate_support_region)`.
- Transfer rationale: tests the learned elevated cabinet-top pickup followed by the new dining-set destination.
- Result: **4/5 (80%)**; episode 0 failed, episodes 1–4 succeeded.

### DSET_004

- Full instruction: **Pick up the ramekin at the table center and place it on the dining-set mat.**
- Scene source: `LIBERO_SPATIAL_03`.
- Manipulated object: `glazed_rim_porcelain_ramekin_1` (`glazed_rim_porcelain_ramekin`).
- Initial relation: `On(glazed_rim_porcelain_ramekin_1, main_table_table_center)`.
- Goal: `On(glazed_rim_porcelain_ramekin_1, dining_set_group_1_plate_support_region)`.
- Transfer rationale: replaces the source black bowl at the identical learned pickup pose. The same ramekin-at-center transfer previously reached 5/5 on a plate (`ANLGX_088`).
- Result: **5/5 (100%)**.

### DSET_005

- Full instruction: **Pick up the white bowl at the table center and place it on the dining-set mat.**
- Scene source: `LIBERO_SPATIAL_03`.
- Manipulated object: `white_bowl_1` (`white_bowl`).
- Initial relation: `On(white_bowl_1, main_table_table_center)`.
- Goal: `On(white_bowl_1, dining_set_group_1_plate_support_region)`.
- Transfer rationale: exploratory bowl-shape generalization; `white_bowl` was not a manipulated object in the original LIBERO-40 training tasks.
- Result: **1/5 (20%)**; episode 4 succeeded, episodes 0–3 failed.

## Aggregate result

- Five tasks, 25 unique episodes.
- 20 successes and 5 failures: **80.0%**.
- Every task has at least one success.
- All 25 original outcome videos are retained: 20 success videos and 5 failure videos.
- Every MP4 was decoded from its first and final frame: 512×304, 5 FPS, no unreadable files.
- No GitHub or anonymous review-page upload was performed for this batch.

## Local artifacts

- Success-video manifest: `evaluation_5ep/success_videos.tsv`
- Success videos: `evaluation_5ep/success_videos/<TASK_ID>/`
- Failure-video manifest: `evaluation_5ep/failure_videos.tsv`
- Failure videos: `evaluation_5ep/failure_videos/<TASK_ID>/`
- Per-task rates: `evaluation_5ep/task_success_rates.tsv`
- All episode outcomes: `evaluation_5ep/episodes.tsv`
- Full audited aggregate: `evaluation_5ep/raw_results/aggregate.json`
- Task definitions and five initial states: `tasks/<task_bundle>/`
