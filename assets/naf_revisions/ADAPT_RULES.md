# NAF Revision Re-evaluation

4 simulator-valid single-goal tasks from 4 raw candidates.

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
- Evaluate five episodes/task with the established RAIN multi-scale + mask-augmentation checkpoint on physical GPUs 6/7; retain every success and one original-trial failure/task when a failure exists.


## Evaluation and build disclosure

4 accepted tasks from 4 proposed; 0 excluded before evaluation.

- [Build audit](BUILD_VALIDATION.json)
- [Pre-evaluation exclusions](REJECTED_CANDIDATES.tsv)
- [Raw-to-accepted IDs](RAW_TO_FINAL_IDS.tsv)

## Scene and asset scope

This page reports exactly the four requested revisions and their original five policy trials. NAFR_001 keeps the NAF_017 popcorn pose and adds three nearby package objects. NAFR_002 keeps the NAF_036 yellow-book pose and adds one black book. NAFR_003 keeps the NAF_054 cabinet pose and drawer initialization while adding one stove and two plates. NAFR_004 removes the LIBERO_10_03 moka pot, moves the frying pan to the exact removed moka-pot region, and evaluates pan placement only. Every successful episode is included. Exactly one failure clip from the same five trials is included for each task that had a failure; NAFR_002 has none because it succeeded in all five episodes.
