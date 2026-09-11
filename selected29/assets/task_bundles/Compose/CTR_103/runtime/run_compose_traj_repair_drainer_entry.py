#!/usr/bin/env python3
"""Preserve the historical strict drainer observer inside the repair trace/replay.

Import order is deliberate: the established ordered replay captures V3's
released-and-supported episode runner, then the observation-only tracer wraps
both. Native early success cannot bypass the existing release/support gate.
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent/'RAIN'))
import run_bowl_drainer_compose_visibility_v3_evaluator_entry as drainer
import run_compose_traj_repair_evaluator_entry as trace

if trace.ordered.ordered._episode is not drainer.visibility_episode:
    raise RuntimeError('Strict drainer runner was not captured before replay/trace')

if __name__ == '__main__':
    trace.exact.evaluator.main()
