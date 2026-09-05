# Novel Scene Adapt

36 simulator-valid single-goal tasks from 36 raw candidates.

## Rules

- Transfer one demonstrated skill/relation from original LIBERO-40; one goal atom, not an action-level conjunction.
- Vary fixture pose, pickup support, reference frame, push direction, receptacle/context binding, or exact fixture instance.
- Keep nonblocking context. Remove documented actual body/approach/swing obstructions only.
- Drawer insertion/extraction and closure prerequisites are explicitly initialized, not extra subtasks.
- Five distinct settled initial states per task: required support/articulation predicates true; goal false; every exact target mask visible.
- Initial closed drawers may settle within 8 mm of q=0 and must not satisfy Open; this handles stock Close sign-boundary contact jitter. Evaluation success predicates are never relaxed.
- Fixture controls use exact articulated part masks. Relative placement/push masks use the current task BDDL region, not a stored source mask.
- Compare against original40, Analogy, expanded Analogy, Adapt, cross-suite Adapt, finalized tasks, and prior object variants using normalized physical-init + goal signatures; this is exact-definition deduplication, not a claim that similar skills never repeat.
- Comparison PNGs separate skill provenance from scene provenance and show both original and new masks.
- Evaluate five episodes/task with the established RAIN multi-scale + mask-augmentation checkpoint on physical GPUs 2/3; retain up to five successes and one original-trial failure/task.



## Evaluation and build disclosure

36 accepted tasks from 36 proposed; 0 excluded before evaluation.

- [Build audit](BUILD_VALIDATION.json)
- [Pre-evaluation exclusions](REJECTED_CANDIDATES.tsv)
- [Raw-to-accepted IDs](RAW_TO_FINAL_IDS.tsv)
- [Novelty audit](NOVELTY_VALIDATION.json)
- [Asset inventory](ASSET_INVENTORY.tsv)
- [LIBERO-90 definitions](BASELINE90_TASK_CATALOG.tsv)
- [Exact mask binding audit](MASK_ALIGNMENT_STATIC_AUDIT.json)
- [Mask renderer equivalence](MASK_RENDERER_EQUIVALENCE.json)

## Scene and asset scope

Novel scenes fully rebuild furniture, objects, regions, and initial predicates; only the original workspace, robot, and camera frame remain. Exact task, scene, and asset-composition signatures are checked against original40 and LIBERO90; shared primitive skills are intentional. Popcorn and macaroni are absent from both suites. Yellow book, wooden tray, and new salad dressing are absent from40 but present in90, so their object identities alone are not claimed novel relative to90. Original40 comparison images document skill/workspace provenance, not unchanged scenes. Native-site destination masks are exact current-simulator projected box silhouettes, not claims of occlusion-visible surface segmentation.
