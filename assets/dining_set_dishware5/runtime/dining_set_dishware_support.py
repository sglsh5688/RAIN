"""Process-local support for dishware-on-dining-set tasks.

The installed ``dining_set_group`` asset is never edited.  This module reuses
the audited physical cloth support site and fixed-fixture height correction
from the Novel Adapt feedback benchmark, then adds exact RAIN bindings for the
three manipulated dishware categories used by this small follow-up screen.
"""

from __future__ import annotations

from copy import deepcopy


TARGET_REGION = "dining_set_group_1_plate_support_region"


def install_dining_set_dishware_support() -> None:
    """Install the audited dining-set support geometry in this process."""
    from novel_feedback_fixture_geometry import install_feedback_fixture_geometry

    install_feedback_fixture_geometry()


def register_object_bindings(action_objects=None):
    """Register exact object bodies and the nonsegmentable physical site."""
    from novel_feedback_object_bindings import register_object_bindings as register_feedback

    action_objects = register_feedback(action_objects)
    additions = {
        "akita_black_bowl_1": {
            "name": "akita_black_bowl_1",
            "body_name": "akita_black_bowl_1_main",
            "body_ids": [0],
            "geom_ids": [],
            "segmentable": True,
        },
        "glazed_rim_porcelain_ramekin_1": {
            "name": "glazed_rim_porcelain_ramekin_1",
            "body_name": "glazed_rim_porcelain_ramekin_1_main",
            "body_ids": [0],
            "geom_ids": [],
            "segmentable": True,
        },
        "white_bowl_1": {
            "name": "white_bowl_1",
            "body_name": "white_bowl_1_main",
            "body_ids": [0],
            "geom_ids": [],
            "segmentable": True,
        },
        TARGET_REGION: {
            "name": TARGET_REGION,
            "body_name": TARGET_REGION,
            "body_ids": [],
            "geom_ids": [],
            "segmentable": False,
        },
    }
    action_objects.update(deepcopy(additions))
    return action_objects
