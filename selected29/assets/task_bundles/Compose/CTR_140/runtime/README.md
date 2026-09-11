# CTR_140 required evaluation support

Use the recorded entrypoint `run_compose_traj_repair_dual_stove_entry.py` with this exact task bundle, five frozen initialization states and `FIXTURE_REPLAY.json`. Keep the task ID **CTR_140**, action plan, source instructions, mask bindings, strict ordered goals, final BDDL conjunction and the original 1600-control limit. There is no final TC gate. A generic BDDL-only evaluation is not an equivalent evaluation protocol.

Ordered native On, TurnOn, Open transitions and final native BDDL conjunction. No added five-control support or settling gate is claimed for this task. Exact knob-only action mask and frozen fixture replay must remain intact.

The archived result is 1/5 certified RAIN episodes (indices 3), using the existing RAIN action and progress checkpoints, seeds 7–11. This export performed no new policy evaluation and changes no historical score.

These are source/provenance support files, not a standalone policy package. The directory contains the minimal recursively resolved local Python import closure from the recorded evaluator entrypoint. The two analogy builder modules are imported for their geometry parsing helpers; their scene-generation CLI is not part of evaluation. The original RAIN `final_libero_ex_eval` package and its model dependencies, LIBERO/robosuite/MuJoCo and matching assets, PyTorch, NumPy, PyYAML, Pillow/OpenCV, unchanged action/progress checkpoints and original episode/action-prior data must be installed/configured separately. No model weights, dataset, simulator assets or third-party library trees are included.

Put this directory on `PYTHONPATH` together with the matching RAIN package. Its original sibling-RAIN path assumptions and `/path/to/` placeholders are documentary source paths and must be configured for the receiving environment. Do not execute this export as a new experiment while merely reviewing the selection update.

`RUNTIME_CONTRACT.json` records the local source SHA256 and published-copy SHA256 for every included file, exact saved entrypoint fingerprint verification, the required terminal semantics, and current read-only external RAIN implementation fingerprints. External current hashes are provenance only; they are not falsely represented as historical run-manifest hashes. Published source paths were sanitized with the same `copy_public_file` plus selected-gallery support sanitizer convention. The original source files remain unchanged.
