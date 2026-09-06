# Dining-Set Relocation and Wooden-Tray Object Choices

Seven independently defined tasks were each evaluated for five episodes with the existing RAIN checkpoints on physical GPUs 6 and 7. The 35 initial goals were false. The audited result is 2 successes and 33 failures.

## DSETRP_001 — exact ramekin-position relocation

The glazed-rim porcelain ramekin is removed and the dining-set mat moves from `(0.06, 0.20)` to that ramekin's exact authored center `(-0.20, 0.20)`, a `(-0.26, 0.00)` meter translation. Bowl pickup, remaining scene poses, instruction, and physical `On(akita_black_bowl_1, dining_set_group_1_plate_support_region)` goal are unchanged. The original-position DSET_001 baseline was 5/5 with the same checkpoint hashes; the relocated task was 0/5.

## WTRAY_001–006 — three visible object choices

The native, unscaled wooden tray is centered at `(0.10, 0.00)`. Three visible choices share `x=-0.13`; left/middle/right are at `y=-0.23`, `0.00`, and `+0.23`. WTRAY_001–003 use three plates and select one by position. WTRAY_004–006 co-place a black bowl, ramekin, and white bowl and select one by identity.

WTRAY success is deliberately stricter than stock root-only `In`: native `In(selected, wooden_tray_1_contain_region)` AND the complete collision envelope inside the native site (1 mm tolerance) AND positive-force tray contact AND no gripper contact, held for five consecutive control steps. WTRAY_004 episodes 2 and 4 meet every condition. Native root-only `In` was true in two additional failed rollouts, but full containment or release was absent, so they remain failures.

## Per-task results

### DSETRP_001

- Instruction: Pick up the black bowl at the table center and place it on the dining-set mat.
- Source: `libero_spatial` task 3 — Pick the akita black bowl from table center and place it on the plate
- Goal: `on(akita_black_bowl_1, dining_set_group_1_plate_support_region)`
- Result: 0/5 (0.0%)
- Success episodes: none
- Failure episodes: 0, 1, 2, 3, 4

### WTRAY_001

- Instruction: Pick up the left plate and place it in the wooden tray.
- Source: `libero_10` task 5 — put the white mug on the left plate and put the yellow and white mug on the right plate
- Goal: `in(plate_1, wooden_tray_1_contain_region)`
- Result: 0/5 (0.0%)
- Success episodes: none
- Failure episodes: 0, 1, 2, 3, 4

### WTRAY_002

- Instruction: Pick up the middle plate and place it in the wooden tray.
- Source: `libero_10` task 5 — put the white mug on the left plate and put the yellow and white mug on the right plate
- Goal: `in(plate_2, wooden_tray_1_contain_region)`
- Result: 0/5 (0.0%)
- Success episodes: none
- Failure episodes: 0, 1, 2, 3, 4

### WTRAY_003

- Instruction: Pick up the right plate and place it in the wooden tray.
- Source: `libero_10` task 5 — put the white mug on the left plate and put the yellow and white mug on the right plate
- Goal: `in(plate_3, wooden_tray_1_contain_region)`
- Result: 0/5 (0.0%)
- Success episodes: none
- Failure episodes: 0, 1, 2, 3, 4

### WTRAY_004

- Instruction: Pick up the black bowl and place it in the wooden tray.
- Source: `libero_spatial` task 3 — Pick the akita black bowl from table center and place it on the plate
- Goal: `in(akita_black_bowl_1, wooden_tray_1_contain_region)`
- Result: 2/5 (40.0%)
- Success episodes: 2, 4
- Failure episodes: 0, 1, 3

### WTRAY_005

- Instruction: Pick up the ramekin and place it in the wooden tray.
- Source: `libero_spatial` task 3 — Pick the akita black bowl from table center and place it on the plate
- Goal: `in(glazed_rim_porcelain_ramekin_1, wooden_tray_1_contain_region)`
- Result: 0/5 (0.0%)
- Success episodes: none
- Failure episodes: 0, 1, 2, 3, 4

### WTRAY_006

- Instruction: Pick up the white bowl and place it in the wooden tray.
- Source: `libero_spatial` task 3 — Pick the akita black bowl from table center and place it on the plate
- Goal: `in(white_bowl_1, wooden_tray_1_contain_region)`
- Result: 0/5 (0.0%)
- Success episodes: none
- Failure episodes: 0, 1, 2, 3, 4
