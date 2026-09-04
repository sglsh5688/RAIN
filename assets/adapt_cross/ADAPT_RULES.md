# LIBERO Adapt cross-suite extension

Atomic skills learned in LIBERO-10 are transferred into Goal, Spatial, and Object source scenes. Every comparison explicitly separates the skill source from the destination scene source.

- Accepted simulator-valid candidates: **74**
- Rejected during signature/init screening: **3**
- Five stable init states/task
- Exact current-simulator masks; microwave close is door-only
- Task-only instructions: no scene/layout/while metadata in policy language
- No exact duplicates with Adapt192, original LIBERO-40, or finalized Decomposition20

## Families

| Family | Tasks |
|---|---:|
| `X1_long_to_goal_plate` | 2 |
| `X2_long_to_goal_stove` | 1 |
| `X3_long_to_goal_drawer` | 2 |
| `X4_long_to_goal_caddy` | 2 |
| `X5_long_to_goal_microwave` | 2 |
| `X6_long_to_spatial_plate` | 20 |
| `X7_long_to_spatial_stove` | 9 |
| `X8_long_to_spatial_close` | 6 |
| `X9_long_to_object_basket` | 30 |

## Provenance contract

- `LONG SKILL SOURCE`: original LIBERO-10 task containing the transferred atomic action.
- `GOAL/SPATIAL/OBJECT SCENE SOURCE`: original task providing the destination physical scene.
- `FIXTURE-POSE SOURCE`: official reachable pose reused when a fixture must be imported.
- Only a geometrically overlapping fixture is removed; unrelated scene entities remain.

See `CROSS_SUITE_PROVENANCE.tsv`, `TASK_INDEX.tsv`, and `comparison_png/`.
