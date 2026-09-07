# Independent review — VCN91_002 ep002

Reviewed 2026-09-07 UTC by the Batch93 agent, independently of the task builder and root's original review. **Verdict: valid full three-action success in this episode.** The task's five-episode result is **1/5 (20%)**, not five successes.

Instruction: “Put the black bowl on top of the cabinet, then turn on the stove, then put the moka pot on the stove.”

## Video and semantic evidence

Reviewed the saved original-frame contact sheet against the raw episode trace and native predicate records. The visible sequence is a deliberate bowl pickup and cabinet-top placement, a separate interaction with the stove knob (the burner visibly turns red), and a moka-pot pickup and placement on that burner. The bowl remains on the cabinet through the final frame. No accidental drawer closure or pre-completed action is involved.

| Check | Recorded evidence |
| --- | --- |
| Initial native goals | `[false, false, false]` |
| Bowl on cabinet first true | Control step140 |
| Stove on first true | Control step300 |
| Moka on stove first true | Control step445 |
| Ordered completion | All three events in requested order; no violation |
| Final native goals | `[true, true, true]`; final BDDL success true |
| Frozen-layout replay error | 0m |
| Final TC gate | Disabled |

Full video: [VCN91_002_ep002_ok.mp4](VCN91_002/VCN91_002_ep002_ok.mp4)

Absolute path:

```text
LIBERO_EX_ICRA27/COMPOSE_SOURCEMIX91_93_REVIEW/VCN91_002/VCN91_002_ep002_ok.mp4
```

Independently recomputed full-file SHA-256:

```text
f70be967bf36c57fc60f5289250594656feeeecbb84f4546a4e9ef15809a06f1
```

The raw record is under `private_evaluation_results/rain_ms_maskaug_gt_valid_compose_new_batch91_top3_5ep_20260907/tasks/all2/VCN91_002/partial/`. The consolidated [EPISODES.json](VCN91_002/EPISODES.json) agrees with the raw ep002 event sequence.

## Source provenance and masks

The Original40 catalog independently matches the comparison labels:

- `LIBERO_GOAL_05`: “Put the bowl on the top of the drawer,” BDDL `put_the_bowl_on_top_of_the_cabinet`.
- `LIBERO_10_03`: “turn on the stove and put the moka pot on it,” BDDL `KITCHEN_SCENE3_turn_on_the_stove_and_put_the_moka_pot_on_it`.

The physical transfer report records the Goal bowl/cabinet pair and K3 moka/stove pair at exact same-index robot-frame source poses across all five states: zero reported position error and zero arbitrary XYZ offset. Only K3's frying pan was removed. This preserves learned atomic interactions while combining the scenes; it is not a claim that the complete new sequence was demonstrated during training.

The runtime turn-on stage records `mask_source=sim_seg_stove_knob`. The comparison's yellow stove indicates the moka placement target, while cyan indicates the knob control; a yellow full-stove placement overlay does not mean turn-on inference used a full-stove mask.

**PNG caveat:** [comparison.png](VCN91_002/comparison.png) combines masked Original40 **source-reference catalog PNGs** and the new scene's physical state0 image. It is not an episode002-specific replay of all three scenes. The source IDs are correct, but those reference pictures should not be used as exact ep002 pose evidence; the frozen-state transfer and runtime replay records provide that evidence.

## Selected overlap and novelty scope

The current `LIBERO_EX_ANONYMOUS_REVIEW/selected29/tasks.tsv` contains18 Compose tasks. Independently inspected snapshot SHA-256:

```text
1ce2c582f029f8f02aa2b9d6f781fde3c039e5debea4aa9fc3fcfca8bb9e6267
```

- **Literal instruction / complete pattern:** No existing Selected Compose entry has this instruction or the complete bowl→cabinet, turn-on, moka→stove combination.
- **Partial overlaps:** `MKDC_001` and `VCN21_001` share moka→stove but then close a drawer or microwave; `VCN9_010` shares stove interaction but places cheese and then turns it on. These are shared primitives, not identical complete combinations.
- **Original LIBERO:** The turn-on→moka suffix is deliberately the original K3 sequence. The preceding Goal bowl→cabinet action makes the complete union different from that original task. Do not describe the suffix itself as novel.
- **Within this batch:** `VCN91_001` and `VCN91_005` use the same goal set with different ordering. They are order controls, not additional distinct task topologies.
- **Historical scope:** A bounded textual scan of existing `LiberoValidComposeNew20260905` candidate/index TSVs found the matching bowl→cabinet / turn-on / moka chain only in Batch91. This is **not** an exhaustive semantic novelty proof over every historical trial or every possible paraphrase.

The evidence supports presenting VCN91_002 as a successful user-requested cross-suite union not already present in the current Selected18 complete patterns, while leaving final selection to the user.

This audit made no changes to `MANUAL_SUCCESS_REVIEW.json`, Selected files, Git state or evaluation code, and launched no additional inference.
