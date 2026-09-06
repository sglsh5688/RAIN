#!/usr/bin/env python3
"""Evaluate the reachable-pose wooden-tray revisions with the RAIN protocol.

This is a deliberately thin, closed-scope supervisor over the already audited
``WTRAY_001..006`` RAIN / strict-physics evaluator.  It changes only the
benchmark inventory, task-ID namespace, result root, and display label.  The
RAIN checkpoints, exact current-simulator masks, controller settings, and
strict five-control-step physical success observer remain identical.

The complete ``WTRAYR_001..006`` inventory is required, each task is evaluated
on all five saved initial states, physical GPUs 6 and 7 are required, and all
five original outcome videos per task are retained.
"""

from __future__ import annotations

import signal
from pathlib import Path

import run_libero_wooden_tray_object_choices_gt_5ep as base


ROOT = Path(__file__).resolve().parent
BENCHMARK = ROOT / "LiberoWoodenTrayObjectChoicesReachable"
RESULT_ROOT = BENCHMARK / "evaluation_5ep" / "raw_results"
ID_PREFIX = "WTRAYR"
LABEL = "Wooden-Tray Object Choices Reachable-Pose Revision"
EXPECTED_IDS = [f"{ID_PREFIX}_{index:03d}" for index in range(1, 7)]


def configure() -> None:
    """Bind the audited WTRAY supervisor to only the reachable revision."""
    base.BENCHMARK = BENCHMARK
    base.RESULT_ROOT = RESULT_ROOT
    base.ID_PREFIX = ID_PREFIX
    base.LABEL = LABEL
    base.EXPECTED_IDS = EXPECTED_IDS
    base.configure()

    # The original supervisor remains a dependency because this wrapper calls
    # its validation, launch, aggregation, and strict audit functions.  Include
    # this scope-binding file as an additional frozen dependency in run_config.
    base.shared.ENTRYPOINT_DEPENDENCIES = [
        *base.shared.ENTRYPOINT_DEPENDENCIES,
        Path(__file__).resolve(),
    ]


def main() -> None:
    configure()
    base.shared.configure = lambda: None
    base.shared.main()


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, base.shared.common.stop_all)
    signal.signal(signal.SIGINT, base.shared.common.stop_all)
    main()
