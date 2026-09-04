# LIBERO-EX anonymous task review

Open `index.html`, or enable GitHub Pages for this repository root.

- `original40/`: all 40 original tasks with exact simulator interaction masks
- `decomposition20/`: finalized 20-task Decomposition review
- `analogy185/`: all 195 evaluated Analogy trials (legacy URL retained), including 10 LIBERO-EX object position swaps
- `analogy_success70/`: the 76 Analogy tasks with at least one success (legacy URL retained)

- `composition439/`: all 439 evaluated Composition trials
- `composition_success/`: 4 Composition tasks with at least one success

- `composition2step_success20/`: 20 successful tasks from the independently evaluated 361-task two-step pool (28 success videos)
- `composition_failures/`: one representative failure video for every Composition task
- `composition_two_step/`: 49 failed three-step tasks with simultaneous two-goal diagnostic evidence; not an independent two-step evaluation

Comparison previews use shared sprite sheets to stay below Anonymous GitHub's 350 requests per 15 minutes limit. Full-resolution PNGs and videos load only when explicitly opened or played.

No checkpoints are included. Stove turn actions use knob-only GT masks.

<!-- ADAPT_README_START -->
- `adapt192/`: all 192 evaluated atomic Adapt candidates (960 episodes)
- `adapt_success/`: Adapt candidates with at least one success (50 tasks, 151 successful episodes)
- Adapt media policy: 20 previews per JPEG sprite, one on-demand video player, and one concatenated success reel per task; `preload=none` prevents eager video requests.
<!-- ADAPT_README_END -->

<!-- COMPOSE_README_START -->
- `compose350/`: all 350 newly evaluated Compose candidates (1,750 episodes)
- `compose_success/`: 3 successful new tasks (7 successful episodes)
- `compose_selected20/`: final 20 successful tasks, retaining fixed `COMP2_001` and `COMP2_012`
- Complete BDDL/init/metadata/mask/action-plan bundles are linked per task.
- Media policy: 20 previews per JPEG sprite and one on-demand concatenated success reel per task.
<!-- COMPOSE_README_END -->
