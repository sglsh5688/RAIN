# Bowl Drainer Either-Compartment Object Variations

## Construction and success semantics

Each task retains the complete corresponding LIBERO-Object target and distractor layout. The learned basket is removed and the rigid `bowl_drainer` is placed at the same center `(0.0, 0.26)` and yaw.

The BDDL-facing `any_compartment_region` is bookkeeping only. Runtime success is `In(object, native left_region) OR In(object, native right_region)`. A representative simulator audit confirms that both compartment centers succeed while the divider midpoint fails. The policy destination mask is the exact projected union of the same two native sites. No asset XML, collision geometry, or native site was edited.

Every task has five distinct saved initial states. All 25 evaluation episodes began with the goal false and a nonempty current-simulator target mask. Evaluation used the existing RAIN multi-scale mask-augmentation checkpoints on physical GPUs 6 and 7, with 520 control steps per episode.

## Results

Five tasks, 25 episodes, 16 successes, 9 failures, 64.0% overall success. Every original episode video is included.

### BDRAIN_001

- Task: Pick the alphabet soup and place it in either compartment of the bowl drainer.
- Source: `LIBERO_OBJECT_01` — Pick the alphabet soup and place it in the basket
- Target: `alphabet_soup_1`
- Pickup center: `(-0.12, -0.24)`
- Distractors: salad dressing, cream cheese, milk, tomato sauce, butter
- Goal: `in(alphabet_soup_1, bowl_drainer_1_any_compartment_region)` interpreted as native left OR native right compartment
- Result: 4/5 (80.0%)
- Successful episodes: 0, 2, 3, 4
- Failed episodes: 1

### BDRAIN_002

- Task: Pick the cream cheese and place it in either compartment of the bowl drainer.
- Source: `LIBERO_OBJECT_02` — Pick the cream cheese and place it in the basket
- Target: `cream_cheese_1`
- Pickup center: `(0.05, -0.1)`
- Distractors: alphabet soup, milk, tomato sauce, butter, orange juice
- Goal: `in(cream_cheese_1, bowl_drainer_1_any_compartment_region)` interpreted as native left OR native right compartment
- Result: 3/5 (60.0%)
- Successful episodes: 1, 2, 3
- Failed episodes: 0, 4

### BDRAIN_003

- Task: Pick the tomato sauce and place it in either compartment of the bowl drainer.
- Source: `LIBERO_OBJECT_06` — Pick the tomato sauce and place it in the basket
- Target: `tomato_sauce_1`
- Pickup center: `(0.05, -0.1)`
- Distractors: milk, butter, orange juice, chocolate pudding, BBQ sauce
- Goal: `in(tomato_sauce_1, bowl_drainer_1_any_compartment_region)` interpreted as native left OR native right compartment
- Result: 3/5 (60.0%)
- Successful episodes: 1, 2, 4
- Failed episodes: 0, 3

### BDRAIN_004

- Task: Pick the butter and place it in either compartment of the bowl drainer.
- Source: `LIBERO_OBJECT_07` — Pick the butter and place it in the basket
- Target: `butter_1`
- Pickup center: `(-0.12, -0.24)`
- Distractors: tomato sauce, orange juice, chocolate pudding, BBQ sauce, ketchup
- Goal: `in(butter_1, bowl_drainer_1_any_compartment_region)` interpreted as native left OR native right compartment
- Result: 3/5 (60.0%)
- Successful episodes: 1, 2, 4
- Failed episodes: 0, 3

### BDRAIN_005

- Task: Pick the chocolate pudding and place it in either compartment of the bowl drainer.
- Source: `LIBERO_OBJECT_09` — Pick the chocolate pudding and place it in the basket
- Target: `chocolate_pudding_1`
- Pickup center: `(-0.12, -0.24)`
- Distractors: orange juice, BBQ sauce, ketchup, salad dressing, alphabet soup
- Goal: `in(chocolate_pudding_1, bowl_drainer_1_any_compartment_region)` interpreted as native left OR native right compartment
- Result: 3/5 (60.0%)
- Successful episodes: 0, 2, 4
- Failed episodes: 1, 3
