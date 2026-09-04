# LIBERO Adapt provenance audit

The original review conflated the scene/template source with the task that taught the transferred skill. This audit separates skill, sibling-part, scene, object-interaction, and pose evidence. Each comparison PNG now shows every relevant original LIBERO-40 source before the evaluated Adapt scene.

## Result

- Tasks audited: **192**
- Eligible after exact-overlap check: **188**
- Exact Decomposition overlaps flagged for exclusion: **2**
- Training-evidence manual review: **2**
- Evidence panels/task: **{1: 26, 2: 119, 3: 43, 4: 4}**
- `ADAPT_057`: skill source is `LIBERO_GOAL_04`; `LIBERO_SPATIAL_10` is separately labeled as scene source.
- `ADAPT_076`: close skill/source scene is `LIBERO_10_04`; its bottom-drawer close is transferred to the middle sibling.

## Review flags

- `NO_DIRECT_MANIPULATION_SOURCE:red_coffee_mug_1`: 2
- `OBJECT_PRESENT_BUT_NEVER_MANIPULATED_IN_LIBERO40`: 2

See `PROVENANCE_AUDIT.tsv` for all 192 task-level mappings and `DUPLICATE_AUDIT.md` for overlap details.
