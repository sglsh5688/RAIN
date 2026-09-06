# LIBERO-EX anonymous task review

<!-- SELECTED29_README_START -->
- `selected29/`: **Selected Tasks — 20 Decomposition + 17 Adapt + 13 Compose (50 total)**; historical RAIN records, a separate official π0.5 LIBERO-40 5-episode evaluation, representative success/failure videos, masked comparisons and downloadable definitions.
<!-- SELECTED29_README_END -->

Open `index.html`, or enable GitHub Pages for this repository root.

- `original40/`: all 40 original tasks with exact simulator interaction masks

- `composition439/`: all 439 evaluated Composition trials
- `composition_success/`: 4 Composition tasks with at least one success

- `composition2step_success20/`: 20 successful tasks from the independently evaluated 361-task two-step pool (28 success videos)
- `composition_failures/`: one representative failure video for every Composition task
- `composition_two_step/`: 49 failed three-step tasks with simultaneous two-goal diagnostic evidence; not an independent two-step evaluation

Comparison previews use shared sprite sheets to stay below Anonymous GitHub's 350 requests per 15 minutes limit. Full-resolution PNGs and videos load only when explicitly opened or played.

No checkpoints are included. Stove turn actions use knob-only GT masks.


<!-- ADAPT_CROSS_README_START -->
- `adapt_cross_success/`: 46 candidates with success (158 successful episodes)
- Media: shared preview sprites, `preload=none`, and one on-demand concatenated reel per task.
<!-- ADAPT_CROSS_README_END -->


<!-- COMPOSE_README_START -->
- `compose_success/`: all 6 successful tasks (14 successful episodes); no final selection applied
- `compose350/`: all 666 evaluated Compose candidates, including successes and failures (3,330 episodes)
- Complete BDDL/init/metadata/mask/action-plan bundles are linked per task.
- Media policy: 20 previews per JPEG sprite and one on-demand concatenated success reel per task.
<!-- COMPOSE_README_END -->


<!-- ADAPT_README_START -->
- `adapt192/`: all 192 evaluated atomic Adapt candidates (960 episodes)
- `adapt_success/`: Adapt candidates with at least one success, excluding selected tasks (42 tasks, 125 successful episodes)
- Adapt media policy: 20 previews per JPEG sprite, one on-demand video player, and one concatenated success reel per task; `preload=none` prevents eager video requests.
<!-- ADAPT_README_END -->

<!-- DIVERSE_ADAPT_NOVEL_README_START -->
- `diverse_adapt_novel_all/`: all 36 Novel Scene Adapt tasks, including zero-success tasks; five original trials per task.
- `diverse_adapt_novel_success/`: 2 tasks with success, 6 successful episodes.
- Shared JPEG preview sprites, one on-demand player (`preload=none`), success reels and one original-trial failure clip when a task failed.
<!-- DIVERSE_ADAPT_NOVEL_README_END -->

<!-- NOVEL_ADAPT_FEEDBACK_README_START -->
- `novel_adapt_feedback_all/`: all 56 Novel Adapt Feedback tasks, including zero-success tasks; five original trials per task.
- `novel_adapt_feedback_success/`: 11 tasks with success, 34 successful episodes.
- Shared JPEG preview sprites, one on-demand player (`preload=none`), success reels and one original-trial failure clip when a task failed.
<!-- NOVEL_ADAPT_FEEDBACK_README_END -->



<!-- BOWL_DRAINER_ANY5_README_START -->
- `bowl_drainer_any5/`: five bowl-drainer either-compartment tasks; 16/25 successes.
- Includes full construction/success semantics, complete task bundles, and all 16 success plus 9 failure videos.
<!-- BOWL_DRAINER_ANY5_README_END -->




<!-- BOWL_DRAINER_SECTIONS_README_START -->
- `bowl_drainer_sections/`: 10 left/right compartment tasks, all 50 original episodes; 49/50 native successes.
- `bowl_drainer_sections_success/`: 49 native-success videos, masked comparisons and contact diagnostics.
- Native `In` entry terminates these episodes; stable landing/settled placement is **not validated**.
<!-- BOWL_DRAINER_SECTIONS_README_END -->

<!-- BOWL_DRAINER_COMPOSE_README_START -->
## Bowl Drainer — Strict Composition Successes

- [Composition: strict-success episodes only](bowl_drainer_compose_success/index.html)
<!-- BOWL_DRAINER_COMPOSE_README_END -->

<!-- VALID_COMPOSE_NEW_README_START -->
- `valid_compose_new/`: 3 fresh strict-success Compose candidates, 10 successful episodes.
- Each card links the masked comparison, complete public task bundle, and one on-demand reel containing all success episodes.
<!-- VALID_COMPOSE_NEW_README_END -->

<!-- BATCH19_PENDING_README_START -->
- `valid_compose_new_batch19_review/`: 1 manually inspected Batch19 pending-review task(s), 1 strict-success episode(s); not final-selected.
<!-- BATCH19_PENDING_README_END -->
