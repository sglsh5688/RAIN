#!/usr/bin/env python3
"""RAIN evaluator entrypoint with exact metadata for new Analogy instances."""

from __future__ import annotations

from final_libero_ex_eval.impl import benchmark_support


# These exact instances / sibling regions are intentionally new to the
# Analogy candidate registry and are absent from the static LIBERO-EX object
# table.  Supplying their real simulator body names lets the exact simulator
# segmentation path resolve them without source-episode JSON fallback.
EXTRA_ACTION_OBJECTS = {
    "plate_3": {
        "name": "plate_3_main",
        "body_name": "plate_3_main",
        "body_ids": [0],
        "geom_ids": [],
        "segmentable": True,
    },
    "wooden_cabinet_1_bottom_region": {
        "name": "wooden_cabinet_1_cabinet_bottom",
        "body_name": "wooden_cabinet_1_cabinet_bottom",
        "body_ids": [0],
        "geom_ids": [],
        "segmentable": True,
    },
    "akita_black_bowl_3": {
        "name": "akita_black_bowl_3_main",
        "body_name": "akita_black_bowl_3_main",
        "body_ids": [0],
        "geom_ids": [],
        "segmentable": True,
    },
    "chefmate_8_frypan_1": {
        "name": "chefmate_8_frypan_1_main",
        "body_name": "chefmate_8_frypan_1_main",
        "body_ids": [0],
        "geom_ids": [],
        "segmentable": True,
    },
    "desk_caddy_1_front_contain_region": {
        "name": "desk_caddy_1_main",
        "body_name": "desk_caddy_1_main",
        "body_ids": [0],
        "geom_ids": [],
        "segmentable": True,
    },
    "desk_caddy_1_left_contain_region": {
        "name": "desk_caddy_1_main",
        "body_name": "desk_caddy_1_main",
        "body_ids": [0],
        "geom_ids": [],
        "segmentable": True,
    },
    "desk_caddy_1_right_contain_region": {
        "name": "desk_caddy_1_main",
        "body_name": "desk_caddy_1_main",
        "body_ids": [0],
        "geom_ids": [],
        "segmentable": True,
    },
}

benchmark_support.ACTION_OBJECTS.update(EXTRA_ACTION_OBJECTS)

from final_libero_ex_eval.impl.evaluator import main  # noqa: E402


if __name__ == "__main__":
    main()
