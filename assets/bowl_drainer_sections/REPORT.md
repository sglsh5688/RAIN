# Bowl Drainer — Robot-Left / Robot-Right Sections

10 tasks × 5 original episodes, GPUs 6/7. Native-predicate SR: 49/50 episodes (98.0%), 10/10 tasks with at least one native success.

## IMPORTANT: native success is not proof of settled placement

The unchanged LIBERO evaluator can terminate immediately when the object's root first enters the selected native compartment volume. 49/49 native-success episodes ended at that first-true step. At the recorded endpoint, 0/49 native-success episodes had drainer contact and 0/49 had floor contact; 49/49 had neither. A clip may therefore stop before the object lands.

**Settled placement has NOT been validated.** These results are the standard native-predicate SR, not a measured settled-placement SR. Contact diagnostics are observational and did not alter the success rule. No post-success settling rollout was performed. Separate manually seeded geometry/placement witnesses demonstrate feasibility only; they are not policy episodes and cannot establish that the evaluated policy completed a stable placement.

## Definition

The five previous either-compartment object variants are each split into two independent tasks. The instruction requests exactly one robot-relative compartment. Success and the destination mask use that one unchanged native compartment only; placing the object in the other compartment does not satisfy the task. Native asset labels and robot-relative left/right are reported separately below.

The drainer pose is adjusted by the task builder so that the requested compartment is aligned with a reachable placement area. Comparison PNGs show the original LIBERO masked scene, the previous either-compartment task, and the new dedicated-compartment scene. Exact poses, masks, and initialization checks are preserved in the downloadable task definitions and audit files.

The new batch also corrects the drainer's vertical support: the simulator's physical floor is z=0, while the logical floor reference is -0.035 m. The new drainer root is z=+0.00602 m, placing its collision bottom on the physical floor; this is a +3.5 cm correction relative to placement from the logical reference. The prior either-compartment benchmark and results remain unchanged. Native collision geometry and site extents are not enlarged.

No extra rollouts were used to find videos. Every original success and failure is included. MP4s are faststart-ready; the review uses one comparison sprite and one initially empty, on-demand video player. A small request count reduces rate-limit exposure but cannot guarantee that the hosting service never rate-limits access.

## Per-task results

| Task ID | Robot-relative side | Native site | Instruction | Native successes | Native SR |
|---|---|---|---|---:|---:|
| BDRSIDE_001 | left | `left_region` | Pick the alphabet soup and place it in the left compartment of the bowl drainer. | 4/5 | 80.0% |
| BDRSIDE_002 | right | `right_region` | Pick the alphabet soup and place it in the right compartment of the bowl drainer. | 5/5 | 100.0% |
| BDRSIDE_003 | left | `left_region` | Pick the cream cheese and place it in the left compartment of the bowl drainer. | 5/5 | 100.0% |
| BDRSIDE_004 | right | `right_region` | Pick the cream cheese and place it in the right compartment of the bowl drainer. | 5/5 | 100.0% |
| BDRSIDE_005 | left | `left_region` | Pick the tomato sauce and place it in the left compartment of the bowl drainer. | 5/5 | 100.0% |
| BDRSIDE_006 | right | `right_region` | Pick the tomato sauce and place it in the right compartment of the bowl drainer. | 5/5 | 100.0% |
| BDRSIDE_007 | left | `left_region` | Pick the butter and place it in the left compartment of the bowl drainer. | 5/5 | 100.0% |
| BDRSIDE_008 | right | `right_region` | Pick the butter and place it in the right compartment of the bowl drainer. | 5/5 | 100.0% |
| BDRSIDE_009 | left | `left_region` | Pick the chocolate pudding and place it in the left compartment of the bowl drainer. | 5/5 | 100.0% |
| BDRSIDE_010 | right | `right_region` | Pick the chocolate pudding and place it in the right compartment of the bowl drainer. | 5/5 | 100.0% |

## Protocol

- Episodes per task: 5
- Physical GPUs: 6, 7
- Maximum control steps: 520
- Mask mode: `one_unchanged_native_bowl_drainer_site_no_union_no_stored_mask`
- Action checkpoint SHA-256: `7232043efb5b6d563def9fa378cd6f16b8e4623e103327605a5203714807252f`
- Progress checkpoint SHA-256: `e35566c8f366b49c79fd4e029b42ccde56438bd270f895fd286482febb605eae`

## Source and episode provenance

### BDRSIDE_001

- Original: LIBERO_OBJECT_01 — Pick the alphabet soup and place it in the basket
- New: Pick the alphabet soup and place it in the left compartment of the bowl drainer.
- Requested side / selected native site: left / `left_region`
- Drainer root XY: `[0.0, 0.19789]`; expected world Z: `0.00602` m
- Native-success episode IDs: 0, 1, 2, 4
- Failed episode IDs: 3
- Native successes with final drainer / floor contact: 0/4 / 0/4. Settled placement: not validated.

| Episode | Native success | Final drainer contact | Final floor contact | Stop step | First selected In step | Termination |
|---:|---|---|---|---:|---:|---|
| 0 | True | False | False | 161 | 161 | env_success |
| 1 | True | False | False | 160 | 160 | env_success |
| 2 | True | False | False | 167 | 167 | env_success |
| 3 | False | False | True | 520 | None |  |
| 4 | True | False | False | 172 | 172 | env_success |

### BDRSIDE_002

- Original: LIBERO_OBJECT_01 — Pick the alphabet soup and place it in the basket
- New: Pick the alphabet soup and place it in the right compartment of the bowl drainer.
- Requested side / selected native site: right / `right_region`
- Drainer root XY: `[0.0, 0.31153]`; expected world Z: `0.00602` m
- Native-success episode IDs: 0, 1, 2, 3, 4
- Failed episode IDs: none
- Native successes with final drainer / floor contact: 0/5 / 0/5. Settled placement: not validated.

| Episode | Native success | Final drainer contact | Final floor contact | Stop step | First selected In step | Termination |
|---:|---|---|---|---:|---:|---|
| 0 | True | False | False | 194 | 194 | env_success |
| 1 | True | False | False | 189 | 189 | env_success |
| 2 | True | False | False | 195 | 195 | env_success |
| 3 | True | False | False | 164 | 164 | env_success |
| 4 | True | False | False | 162 | 162 | env_success |

### BDRSIDE_003

- Original: LIBERO_OBJECT_02 — Pick the cream cheese and place it in the basket
- New: Pick the cream cheese and place it in the left compartment of the bowl drainer.
- Requested side / selected native site: left / `left_region`
- Drainer root XY: `[0.0, 0.19789]`; expected world Z: `0.00602` m
- Native-success episode IDs: 0, 1, 2, 3, 4
- Failed episode IDs: none
- Native successes with final drainer / floor contact: 0/5 / 0/5. Settled placement: not validated.

| Episode | Native success | Final drainer contact | Final floor contact | Stop step | First selected In step | Termination |
|---:|---|---|---|---:|---:|---|
| 0 | True | False | False | 186 | 186 | env_success |
| 1 | True | False | False | 151 | 151 | env_success |
| 2 | True | False | False | 155 | 155 | env_success |
| 3 | True | False | False | 149 | 149 | env_success |
| 4 | True | False | False | 159 | 159 | env_success |

### BDRSIDE_004

- Original: LIBERO_OBJECT_02 — Pick the cream cheese and place it in the basket
- New: Pick the cream cheese and place it in the right compartment of the bowl drainer.
- Requested side / selected native site: right / `right_region`
- Drainer root XY: `[0.0, 0.31153]`; expected world Z: `0.00602` m
- Native-success episode IDs: 0, 1, 2, 3, 4
- Failed episode IDs: none
- Native successes with final drainer / floor contact: 0/5 / 0/5. Settled placement: not validated.

| Episode | Native success | Final drainer contact | Final floor contact | Stop step | First selected In step | Termination |
|---:|---|---|---|---:|---:|---|
| 0 | True | False | False | 152 | 152 | env_success |
| 1 | True | False | False | 154 | 154 | env_success |
| 2 | True | False | False | 148 | 148 | env_success |
| 3 | True | False | False | 155 | 155 | env_success |
| 4 | True | False | False | 153 | 153 | env_success |

### BDRSIDE_005

- Original: LIBERO_OBJECT_06 — Pick the tomato sauce and place it in the basket
- New: Pick the tomato sauce and place it in the left compartment of the bowl drainer.
- Requested side / selected native site: left / `left_region`
- Drainer root XY: `[0.0, 0.19789]`; expected world Z: `0.00602` m
- Native-success episode IDs: 0, 1, 2, 3, 4
- Failed episode IDs: none
- Native successes with final drainer / floor contact: 0/5 / 0/5. Settled placement: not validated.

| Episode | Native success | Final drainer contact | Final floor contact | Stop step | First selected In step | Termination |
|---:|---|---|---|---:|---:|---|
| 0 | True | False | False | 149 | 149 | env_success |
| 1 | True | False | False | 170 | 170 | env_success |
| 2 | True | False | False | 179 | 179 | env_success |
| 3 | True | False | False | 148 | 148 | env_success |
| 4 | True | False | False | 166 | 166 | env_success |

### BDRSIDE_006

- Original: LIBERO_OBJECT_06 — Pick the tomato sauce and place it in the basket
- New: Pick the tomato sauce and place it in the right compartment of the bowl drainer.
- Requested side / selected native site: right / `right_region`
- Drainer root XY: `[0.0, 0.31153]`; expected world Z: `0.00602` m
- Native-success episode IDs: 0, 1, 2, 3, 4
- Failed episode IDs: none
- Native successes with final drainer / floor contact: 0/5 / 0/5. Settled placement: not validated.

| Episode | Native success | Final drainer contact | Final floor contact | Stop step | First selected In step | Termination |
|---:|---|---|---|---:|---:|---|
| 0 | True | False | False | 153 | 153 | env_success |
| 1 | True | False | False | 184 | 184 | env_success |
| 2 | True | False | False | 198 | 198 | env_success |
| 3 | True | False | False | 185 | 185 | env_success |
| 4 | True | False | False | 153 | 153 | env_success |

### BDRSIDE_007

- Original: LIBERO_OBJECT_07 — Pick the butter and place it in the basket
- New: Pick the butter and place it in the left compartment of the bowl drainer.
- Requested side / selected native site: left / `left_region`
- Drainer root XY: `[0.0, 0.19789]`; expected world Z: `0.00602` m
- Native-success episode IDs: 0, 1, 2, 3, 4
- Failed episode IDs: none
- Native successes with final drainer / floor contact: 0/5 / 0/5. Settled placement: not validated.

| Episode | Native success | Final drainer contact | Final floor contact | Stop step | First selected In step | Termination |
|---:|---|---|---|---:|---:|---|
| 0 | True | False | False | 169 | 169 | env_success |
| 1 | True | False | False | 178 | 178 | env_success |
| 2 | True | False | False | 171 | 171 | env_success |
| 3 | True | False | False | 185 | 185 | env_success |
| 4 | True | False | False | 169 | 169 | env_success |

### BDRSIDE_008

- Original: LIBERO_OBJECT_07 — Pick the butter and place it in the basket
- New: Pick the butter and place it in the right compartment of the bowl drainer.
- Requested side / selected native site: right / `right_region`
- Drainer root XY: `[0.0, 0.31153]`; expected world Z: `0.00602` m
- Native-success episode IDs: 0, 1, 2, 3, 4
- Failed episode IDs: none
- Native successes with final drainer / floor contact: 0/5 / 0/5. Settled placement: not validated.

| Episode | Native success | Final drainer contact | Final floor contact | Stop step | First selected In step | Termination |
|---:|---|---|---|---:|---:|---|
| 0 | True | False | False | 214 | 214 | env_success |
| 1 | True | False | False | 203 | 203 | env_success |
| 2 | True | False | False | 178 | 178 | env_success |
| 3 | True | False | False | 177 | 177 | env_success |
| 4 | True | False | False | 252 | 252 | env_success |

### BDRSIDE_009

- Original: LIBERO_OBJECT_09 — Pick the chocolate pudding and place it in the basket
- New: Pick the chocolate pudding and place it in the left compartment of the bowl drainer.
- Requested side / selected native site: left / `left_region`
- Drainer root XY: `[0.0, 0.19789]`; expected world Z: `0.00602` m
- Native-success episode IDs: 0, 1, 2, 3, 4
- Failed episode IDs: none
- Native successes with final drainer / floor contact: 0/5 / 0/5. Settled placement: not validated.

| Episode | Native success | Final drainer contact | Final floor contact | Stop step | First selected In step | Termination |
|---:|---|---|---|---:|---:|---|
| 0 | True | False | False | 169 | 169 | env_success |
| 1 | True | False | False | 160 | 160 | env_success |
| 2 | True | False | False | 171 | 171 | env_success |
| 3 | True | False | False | 168 | 168 | env_success |
| 4 | True | False | False | 167 | 167 | env_success |

### BDRSIDE_010

- Original: LIBERO_OBJECT_09 — Pick the chocolate pudding and place it in the basket
- New: Pick the chocolate pudding and place it in the right compartment of the bowl drainer.
- Requested side / selected native site: right / `right_region`
- Drainer root XY: `[0.0, 0.31153]`; expected world Z: `0.00602` m
- Native-success episode IDs: 0, 1, 2, 3, 4
- Failed episode IDs: none
- Native successes with final drainer / floor contact: 0/5 / 0/5. Settled placement: not validated.

| Episode | Native success | Final drainer contact | Final floor contact | Stop step | First selected In step | Termination |
|---:|---|---|---|---:|---:|---|
| 0 | True | False | False | 168 | 168 | env_success |
| 1 | True | False | False | 172 | 172 | env_success |
| 2 | True | False | False | 176 | 176 | env_success |
| 3 | True | False | False | 177 | 177 | env_success |
| 4 | True | False | False | 168 | 168 | env_success |
