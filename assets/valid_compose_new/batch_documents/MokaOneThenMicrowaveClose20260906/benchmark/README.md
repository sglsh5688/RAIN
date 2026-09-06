# VCN21 moka/microwave Compose benchmark

Physically accepted runnable tasks: **1**. Policy inference has not run at build time.

| ID | Instruction | Ordered native events | Comparison |
|---|---|---|---|
| `VCN21_001` | Put the moka pot on the stove, then close the microwave door. | `on(moka_pot_2,flat_stove_1_cook_region) → close(microwave_1)` | [PNG](comparison_png/VCN21_001__comparison.png) |

- Every admitted task passed five frozen states, same-index robot-frame transfer, initial-false, penetration, support, mask, articulation-sweep and deterministic replay gates.
- `VCN21_001` uses K8 moka_pot_2/stove and K6 open microwave; K8 moka_pot_1 is removed.
- Raw door-sweep contacts at the vacated moka pickup are accepted only because every successful original K8 demonstration terminal moka pose was rigidly replayed on the target stove and separated from the door sweep.
- Runtime success requires strict ordered native rising events, all final BDDL predicates, and direct gripper↔`microdoorroot` contact within the two-control-step close window. Final TC is never a success gate.
