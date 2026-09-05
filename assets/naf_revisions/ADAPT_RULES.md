# NAF Revisions — V3

Four new tasks, five final episodes each on physical GPUs 6/7, following the user's GPU override. Initial-state generation/geometry audits previously used GPUs 5/6; those saved states are unchanged. Previous V1/V2 definitions, checkpoints and results are not modified.

| V3 ID | Previous V2 scene | Articulation / task parent | Evaluated instruction | Correction | Comparison |
|---|---|---|---|---|---|
| NAFR3_001 | NAFR_001 | NAF_017 | Put the popcorn on top of the short fridge. | Place popcorn and its three familiar context objects together with regular grasp-clear gaps; the can stays on the robot-left side. | [PNG](comparison_png/NAFR3_001__comparison.png) |
| NAFR3_002 | NAFR_002 | NAF_036 | Put the yellow book on top of the two-layer wooden shelf. | Place the two existing books side by side at the same robot-relative depth, with a modest gap instead of a diagonal layout. | [PNG](comparison_png/NAFR3_002__comparison.png) |
| NAFR3_003 | NAFR_003 | NAF_056 | Close the bottom drawer of the short cabinet. | Remove only the stove from the V2 drawer context; retain both plates and close the bottom drawer alone. | [PNG](comparison_png/NAFR3_003__comparison.png) |
| NAFR3_004 | NAFR_003 | NAF_054 | Close the top drawer of the short cabinet. | Use the same stove-free cabinet and plate layout; start only the top drawer open and close the top drawer alone. | [PNG](comparison_png/NAFR3_004__comparison.png) |

## Protocol and identity

- New NAFR3 identifiers prevent confusing the new top-drawer task with the old NAFR_004 frying-pan task. The pan is unchanged and is not reevaluated in V3.
- The light/white-page book is the existing native yellow_book, not a new or relabeled white_book asset. The other book remains black_book.
- Each task has one native semantic goal, 520 control steps and five distinct settled/reloaded starts. Every goal must initially be false.
- Only exact interaction targets are policy-masked. Drawer masks include only the corresponding moving drawer, never the cabinet shell or context plates.
- Both drawer variants preserve the exact V2 plate regions and remove the stove. Only the selected drawer begins open.
- Same established RAIN multi-scale/mask-augmentation action and progress checkpoints; final policy evaluation uses GPUs 6/7 only.
- The interrupted V3 GPU5/6 run is retained separately and excluded from final rates/videos. The same twenty starts are evaluated afresh on GPUs6/7 because the user changed the GPU allocation, not because of the previous outcomes.
- Save every successful original episode, at most five/task, plus one actual failure/task when a failure exists. No extra trials are used to acquire videos.
- Original LIBERO, previous V2 and new V3 scenes are shown with masks and instructions. Physics probes are not policy success evidence.
- V1/V2 remain available offline; their trials are not counted in V3 results.


## Evaluation and build disclosure

4 accepted tasks from 4 proposed; 0 excluded before evaluation.

- [Offline V1/V2 evidence and hashes](VERSION_HISTORY.json)
- [Build audit](BUILD_VALIDATION.json)
- [Pre-evaluation exclusions](REJECTED_CANDIDATES.tsv)
- [Raw-to-accepted IDs](RAW_TO_FINAL_IDS.tsv)

## Scene and asset scope

V3 is a separate four-task evaluation with visible IDs NAFR3_001–004, five original trials per task on physical GPUs6/7, the established RAIN checkpoints, and 520 steps per atomic goal. The first two tasks revise popcorn-package gaps and book spacing. The other two close the bottom and top drawers without a stove; the new top-drawer task references NAF_054. NAFR3_004 is not the old NAFR_004 pan task: the V2 pan remains historical only and is not rerun. Every mask uses current simulator geometry. All successes and one actual failure per task with a failure are retained from these same five trials. V1/V2 scenes, outcomes and videos are archived only inside the offline package/ZIP, never mixed into V3 statistics or restored as retired public pages. These rates and videos use only the fresh GPU6/7 evaluation. The interrupted GPU5/6 attempt is excluded and preserved separately. Initial-state geometry was built and validated on GPUs5/6 before the policy-device override; its factual build history is retained.
