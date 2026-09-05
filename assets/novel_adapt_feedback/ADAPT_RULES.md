# Novel Adapt Feedback

56 accepted tasks; five distinct validated starting states per task.

## User rules

- Only family F06 places two plates into the wooden tray. Every other task has one semantic goal.
- Microwave popcorn insertion and microwave closure are separate atomic tasks. Closure starts open, with popcorn already inside.
- Reference original LIBERO-40 fixture/pickup/destination placements. Record the exact source task and coordinate assumptions; a BDDL anchor is not a claim that every new trajectory was trained.
- White storage box placement uses the original Long-10 microwave location; orient its opening toward the reachable approach.
- New targets: drainer compartments, dining-set support, fridge roof, storage-box interior, tray, shelf roof, and short-cabinet drawers.
- No task language about scene metadata, training, or "while" clauses. No added stove or unrelated goal.
- Do not rescale object meshes or accept root-only containment for a plate that physically protrudes outside a drainer compartment.
- Every goal atom starts false; prerequisite supports and open/closed controls are explicitly initialized and rechecked after settling/reloading.
- Exact current-model object/region masks in initialization, PNGs, and inference; microwave controls mask only the moving door, drawers only the corresponding moving drawer.
- Five episodes on physical GPUs 5/6 with the established checkpoint; 520 control steps for one semantic goal, 1040 for two plates.
- Preserve all successes (max five/task) and one actual original-trial failure/task; publish separate success-only/all-trial pages.
- Original Diverse45 remains retired; previous Novel36 results remain unchanged.



## Evaluation and build disclosure

56 accepted tasks from 56 proposed; 0 excluded before evaluation.

- [Drainer destination feasibility (not policy trials)](PLATE_DESTINATION_FEASIBILITY.json)
- [Dining-mat support feasibility (not policy trials)](DINING_PLATE_DESTINATION_FEASIBILITY.json)
- [Cubby mug feasibility (not policy trials)](PORCELAIN_CUBBY_DESTINATION_FEASIBILITY.json)
- [Two-plate tray stacking feasibility (not policy trials)](TWO_PLATE_TRAY_TERMINAL_FEASIBILITY.json)
- [Build audit](BUILD_VALIDATION.json)
- [Pre-evaluation exclusions](REJECTED_CANDIDATES.tsv)
- [Raw-to-accepted IDs](RAW_TO_FINAL_IDS.tsv)

## Scene and asset scope

This is a separate feedback batch; the earlier Novel Scene Adapt36 review remains unchanged. Only group6, placing two distinct plates in the tray, is a two-step task. All other groups are atomic one-goal tasks; grasp/release action-plan steps alone do not make an atomic task a two-goal composition. Original40 evidence identifies the actual workspace, initial-position anchors, or analogous manipulation skill, not a claim that new assets or reorientation trajectories were trained there. Plate-to-drainer goals require real drainer contact and the complete plate collision envelope inside the unchanged native compartment, with the disclosed numerical contact tolerance. Dining-set placement uses the actual mat support surface and a contact-requiring On predicate. Initial-state and terminal destination feasibility probes are separate physical checks, not learned-policy trials or success-rate evidence. In the G5 terminal screenshots, cubby walls occlude the mug; images alone do not establish containment. Numerical native-In, collision-envelope, contact and stability checks establish those witnesses. Only the original five policy episodes per accepted task determine the reported rates and success/failure videos. This feedback policy evaluation uses physical GPUs5/6. Earlier completed physical-feasibility probes retain their actual recorded GPU identifiers; their history is not relabeled. Every mask is computed from current simulator geometry; projected native/custom physical sites are box silhouettes, not claims of occlusion-visible surface segmentation.
