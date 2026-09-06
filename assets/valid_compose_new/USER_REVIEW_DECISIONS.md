# Compose user review decisions — 2026-09-06

This file records the semantic-quality review separately from strict evaluator success. A task can satisfy ordered native predicates yet still be rejected if the observed behavior is an accidental side effect or the composition is redundant.

## Retained candidates

| ID | Instruction | Recorded SR | Decision |
|---|---|---:|---|
| VCN8_008 | Put the chocolate pudding on the black bowl, then open the middle drawer of the cabinet. | 4/5 | Retain as the stronger replacement for the COMP2_001 pattern. |
| VCN9_010 | Put the cream cheese on the stove, then turn on the stove. | 4/5 | Retain. |
| VCN10_001 | Put the cream cheese on the stove, then push the plate to the front of the stove. | 2/5 | Retain. |

## Rejected candidates

- Accidental or weakly initialized drawer closure: `VCN1_006`, `VCN1_010`, `VCN1_014`, `VCN3_001`, `VCN3_003`, `VCN5_003`, `VCN6_002`, `VCN6_003`, `VCN6_004`, `VCN6_005`, `VCN8_012`, `VCN11_015`, `VCN14A_005`, `VCN14A_006`, `VCN14A_008`, `VCN14A_009`.
- Redundant variants of the retained COMP2_001/VCN8_008 family: `VCN8_007`, `VCN8_009`, `VCN8_010`.
- Weaker variants of retained VCN9_010 or VCN10_001: `VCN9_011`, `VCN10_003`, `VCN11_009`, `VCN11_010`, `VCN11_012`, `VCN13_001`, `VCN14A_010`.
- Too close to an original LIBERO-10 action pattern: `VCN11_004`, `VCN11_005`, `VCN11_006`, `VCN13_002`, `VCN13_003`, `VCN13_010`.

## Rules for new candidates

1. A requested close target starts fully open, not in the articulation dead-band and not merely slightly open.
2. The policy must deliberately interact with the requested drawer. Closing it by bumping or moving another drawer is not an acceptable success video.
3. Native ordered rising events and all final BDDL predicates remain necessary, but video-level semantic review is also required before selection.
4. Gripper trajectory alignment is a soft success prior, never a hard exclusion rule.
5. Prefer distinct semantic patterns over object-only substitutions. The final Compose set should include cross-layout combinations like `LBCM_003` and `LBCM_028`.
6. Compose final success has no task-completion-head threshold.

## Requested follow-up families

- Extend the exact successful `VCN10_001` sequence with a meaningful third action, including middle-drawer opening where physically valid.
- Initialize top and bottom drawers fully open; deliberately close the top drawer, place a moka pot on the stove from a learned pickup pose, then deliberately close the bottom drawer.
- After the exact `VCN8_008` pudding-on-bowl prefix, pick up the bowl and move the nested stack to a valid learned destination.
- Put cream cheese or butter on a plate, then push the plate while retaining its contents.
- Mix layouts as in `LBCM_003`/`LBCM_028`, including Goal or Spatial scenes with a basket at a source-aligned, collision-free location.
