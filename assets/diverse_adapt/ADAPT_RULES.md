# LIBERO Diverse Adapt

45 simulator-valid single-goal tasks from 48 raw candidates.

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

45 accepted tasks from 48 proposed; 3 excluded before evaluation.

- [Build audit](BUILD_VALIDATION.json)
- [Pre-evaluation exclusions](REJECTED_CANDIDATES.tsv)
- [Raw-to-accepted IDs](RAW_TO_FINAL_IDS.tsv)
