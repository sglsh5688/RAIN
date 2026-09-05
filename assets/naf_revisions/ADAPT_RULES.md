# NAF Revisions — Corrected V2

Four new five-episode evaluations, physical GPUs 5/6. Prior v1 definitions and results remain unchanged in LiberoNAFRevisions.

| Task ID | Reference | Instruction | Correction | Comparison |
|---|---|---|---|---|
| NAFR_001 | NAF_017 | Put the popcorn on top of the short fridge. | Keep popcorn at its original pickup; space three packages with nominal 17.5 cm intervals and move the tomato-sauce can to the robot-left side of popcorn. | [PNG](comparison_png/NAFR_001__comparison.png) |
| NAFR_002 | NAF_036 | Put the yellow book on top of the two-layer wooden shelf. | Keep the target yellow book; move the black book diagonally into vacant table space instead of lining up the two books. | [PNG](comparison_png/NAFR_002__comparison.png) |
| NAFR_003 | NAF_056 | Close the bottom drawer of the short cabinet. | Use NAF_056 bottom-drawer closure; separate the plates in vacant space and shift the stove 11 cm away from the moving drawer. | [PNG](comparison_png/NAFR_003__comparison.png) |
| NAFR_004 | LIBERO_10_03 | Put the frying pan on the stove. | Align the pan HANDLE with the former moka-pot pickup region, preserving native orientation and leaving clearance from the stove. | [PNG](comparison_png/NAFR_004__comparison.png) |

## Protocol

- All tasks have one native semantic goal; five distinct settled/reloaded starts, each goal initially false.
- Exact current-simulator masks; only the bottom moving drawer for NAFR_003. Distractors never enter policy masks.
- Same established RAIN multi-scale/mask-augmentation checkpoints, 520 control steps per episode.
- Keep all successful videos (at most five/task) and one actual failure/task from these same five trials.
- Comparison panels are original LIBERO / previous v1 / corrected v2, with interaction masks and instructions.
- Scene-geometry diagnostics are not policy trials and are never counted in success rates.


## Evaluation and build disclosure

4 accepted tasks from 4 proposed; 0 excluded before evaluation.

- [Preserved V1 evidence and hashes](VERSION_HISTORY.json)
- [Build audit](BUILD_VALIDATION.json)
- [Pre-evaluation exclusions](REJECTED_CANDIDATES.tsv)
- [Raw-to-accepted IDs](RAW_TO_FINAL_IDS.tsv)

## Scene and asset scope

This page evaluates four corrected V2 scenes, with exactly five new original policy trials per task on physical GPUs5/6. Each task has one atomic goal and a 520-step budget. The established RAIN checkpoints and exact current-simulator mask protocol are unchanged. Original sources and prior revision results remain separate: shared NAFR identifiers identify the requested task slot, not an identical physical task version. The comparison panels document the corrected layouts; only V2 trials determine the V2 rates. All successful original V2 episodes are included, and one actual failure clip is included exactly when that task had a failure. The V1 archive in the standalone offline package preserves its original outcomes and media; no V1 episode is counted as a V2 trial.
