# DSET mat at the removed ramekin position

- Task: `DSETRP_001`
- Instruction: Pick up the black bowl at the table center and place it on the dining-set mat.
- Source mat center: `(0.06, 0.20)`
- New mat center: `(-0.20, 0.20)` — exact authored ramekin center
- Translation: `(-0.26, 0.00) m` in main-table XY
- Removed context object: `glazed_rim_porcelain_ramekin_1`
- Fixed: bowl pickup and remaining context poses, mat yaw, language, goal, and physical support site.
- Five fresh, distinct, settled, visible, initially goal-false states were generated on GPU 6.
- State dimension: `66` → `53` after removing one free body.
- Policy inference has not been run.

## RAIN five-episode result

- Result: `0/5` (`0.0%`) on GPU 6 with seed 7.
- Source-position `DSET_001` baseline: `5/5` with the same RAIN checkpoints.
- Every rollout entered both controller phases and transported the bowl to the relocated mat vicinity, but the bowl settled outside or overhung the valid support site near its +X edge.
- The physical `On` goal was never true in any episode; all five reached 520 steps.
- All five original failure videos and their hashes are retained under `evaluation_5ep/rain_ckpt/raw_results/DSETRP_001/videos/`.
- No GitHub upload was performed.
