# LIBERO Compose feedback: two-cabinet exact-coordinate screen

This pool implements the user's correction to the earlier COMP_197 / X11 construction.

- Left fixture: original LIBERO-10 Kitchen Scene 4 white cabinet, unchanged.
- Right fixture: original LIBERO-Goal wooden cabinet coordinate and yaw, unchanged.
- Wine bottle: original LIBERO-Goal initial coordinate, not the Kitchen Scene 4 coordinate used by the earlier screen.
- Plate interpretation A: move the Goal-position plate onto the left cabinet.
- Plate interpretation B: initialize the plate on the left cabinet and put the bowl on it.
- Evaluation protocol: five fixed init states per task, GPUs 6 and 7 only.

| Semantic steps | Tasks |
|---:|---:|
| 2 | 8 |
| 3 | 11 |
| 4 | 5 |

Total: **24 tasks / 120 episodes**.
