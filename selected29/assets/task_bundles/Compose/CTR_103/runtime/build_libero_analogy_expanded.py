#!/usr/bin/env python3
"""Build the context-preserving LIBERO Analogy expansion.

Relation/layout donors come from LIBERO-Spatial, LIBERO-Goal, and LIBERO-10.
The original LIBERO-Object tasks may provide independent evidence that a
package object was grasped during training.  Source-scene context is retained
by default; an entity is removed only when it physically overlaps a relocated
target or blocks the intended manipulation corridor.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
from collections import OrderedDict
from pathlib import Path
from typing import Callable

import yaml
import numpy as np
from PIL import Image

import build_libero_analogy as base


HERE = Path(__file__).resolve().parent
OUTPUT_ROOT = HERE / "LiberoAnalogyExpanded"
BDDL_ROOT = base.SOURCE_BDDL
INIT_ROOT = base.SOURCE_INIT


def source(suite: str, stem: str) -> tuple[Path, Path]:
    return (
        BDDL_ROOT / suite / f"{stem}.bddl",
        INIT_ROOT / suite / f"{stem}.pruned_init",
    )


SCENE5, SCENE5_INIT = source(
    "libero_10",
    "LIVING_ROOM_SCENE5_put_the_white_mug_on_the_left_plate_and_put_the_yellow_and_white_mug_on_the_right_plate",
)
STUDY1, STUDY1_INIT = source(
    "libero_10",
    "STUDY_SCENE1_pick_up_the_book_and_place_it_in_the_back_compartment_of_the_caddy",
)
KITCHEN3, KITCHEN3_INIT = source(
    "libero_10", "KITCHEN_SCENE3_turn_on_the_stove_and_put_the_moka_pot_on_it"
)
KITCHEN4, KITCHEN4_INIT = source(
    "libero_10",
    "KITCHEN_SCENE4_put_the_black_bowl_in_the_bottom_drawer_of_the_cabinet_and_close_it",
)
KITCHEN6, KITCHEN6_INIT = source(
    "libero_10", "KITCHEN_SCENE6_put_the_yellow_and_white_mug_in_the_microwave_and_close_it"
)
SCENE1, SCENE1_INIT = source(
    "libero_10",
    "LIVING_ROOM_SCENE1_put_both_the_alphabet_soup_and_the_cream_cheese_box_in_the_basket",
)
SCENE2, SCENE2_INIT = source(
    "libero_10",
    "LIVING_ROOM_SCENE2_put_both_the_alphabet_soup_and_the_tomato_sauce_in_the_basket",
)

GOAL_BOWL_PLATE, GOAL_BOWL_PLATE_INIT = source("libero_goal", "put_the_bowl_on_the_plate")
GOAL_CREAM_BOWL, GOAL_CREAM_BOWL_INIT = source("libero_goal", "put_the_cream_cheese_in_the_bowl")
GOAL_OPEN_MIDDLE, GOAL_OPEN_MIDDLE_INIT = source("libero_goal", "open_the_middle_drawer_of_the_cabinet")
GOAL_INSERT_TOP, GOAL_INSERT_TOP_INIT = source("libero_goal", "open_the_top_drawer_and_put_the_bowl_inside")
GOAL_TURN_STOVE, GOAL_TURN_STOVE_INIT = source("libero_goal", "turn_on_the_stove")
GOAL_PUSH_STOVE, GOAL_PUSH_STOVE_INIT = source("libero_goal", "push_the_plate_to_the_front_of_the_stove")
GOAL_BOWL_STOVE, GOAL_BOWL_STOVE_INIT = source("libero_goal", "put_the_bowl_on_the_stove")
GOAL_WINE_RACK, GOAL_WINE_RACK_INIT = source("libero_goal", "put_the_wine_bottle_on_the_rack")
GOAL_BOWL_CABINET, GOAL_BOWL_CABINET_INIT = source("libero_goal", "put_the_bowl_on_top_of_the_cabinet")
GOAL_WINE_CABINET, GOAL_WINE_CABINET_INIT = source("libero_goal", "put_the_wine_bottle_on_top_of_the_cabinet")
SPATIAL_DRAWER, SPATIAL_DRAWER_INIT = source(
    "libero_spatial",
    "pick_up_the_black_bowl_in_the_top_drawer_of_the_wooden_cabinet_and_place_it_on_the_plate",
)
SPATIAL_STOVE, SPATIAL_STOVE_INIT = source(
    "libero_spatial", "pick_up_the_black_bowl_on_the_stove_and_place_it_on_the_plate"
)


def region(name: str, target: str, xy: tuple[float, float, float, float] | None = None, yaw: float | None = None) -> str:
    lines = [f"      ({name}", f"          (:target {target})"]
    if xy is not None:
        values = " ".join(f"{value:.6f}" for value in xy)
        lines.extend(
            [
                "          (:ranges (",
                f"              ({values})",
                "            )",
                "          )",
            ]
        )
    if yaw is not None:
        lines.extend(
            [
                "          (:yaw_rotation (",
                f"              ({yaw:.12f} {yaw:.12f})",
                "            )",
                "          )",
            ]
        )
    lines.append("      )")
    return "\n".join(lines)


def block(section: str, lines: list[str]) -> str:
    body = "\n".join(lines)
    return f"  (:{section}\n{body}\n  )"


def section_body(text: str, section: str, next_section: str) -> str:
    match = re.search(
        rf"^[ \t]*\(:{section}\n(.*?)^[ \t]*\)\n\n[ \t]*\(:{next_section}",
        text,
        flags=re.DOTALL | re.MULTILINE,
    )
    if not match:
        raise ValueError(f"cannot extract section {section}")
    return match.group(1)


def parse_typed_declarations(body: str) -> OrderedDict[str, str]:
    declarations: OrderedDict[str, str] = OrderedDict()
    for raw in body.splitlines():
        line = raw.strip()
        if not line or " - " not in line:
            continue
        names, object_type = line.rsplit(" - ", 1)
        for name in names.split():
            declarations[name] = object_type.strip()
    return declarations


def render_typed_section(section: str, declarations: OrderedDict[str, str]) -> str:
    # LIBERO's BDDL parser overwrites an earlier entry when the same type is
    # declared on a second ``- type`` line.  Group all instances of a type on
    # one line (the format used by the official tasks) so none disappear.
    grouped: OrderedDict[str, list[str]] = OrderedDict()
    for name, kind in declarations.items():
        grouped.setdefault(kind, []).append(name)
    return block(
        section,
        [f"    {' '.join(names)} - {kind}" for kind, names in grouped.items()],
    )


def split_region_chunks(body: str) -> list[str]:
    lines = body.splitlines()
    chunks: list[str] = []
    current: list[str] = []
    balance = 0
    for raw in lines:
        if not current and not raw.strip():
            continue
        if not current:
            current = [raw]
            balance = raw.count("(") - raw.count(")")
        else:
            current.append(raw)
            balance += raw.count("(") - raw.count(")")
        if current and balance == 0:
            chunks.append("\n".join(current).rstrip())
            current = []
    if current:
        raise ValueError("unbalanced region block")
    return chunks


def region_key(chunk: str) -> tuple[str, str]:
    name = re.search(r"^\s*\(([^\s()]+)", chunk)
    target = re.search(r"\(:target\s+([^\s()]+)\)", chunk)
    if not name or not target:
        raise ValueError(f"invalid region block: {chunk[:80]!r}")
    return name.group(1), target.group(1)


def init_expressions(body: str) -> list[str]:
    return [line.strip() for line in body.splitlines() if line.strip()]


def init_subject(expression: str) -> str:
    match = re.match(r"\((?:On|In|Open|Close|Turnon|Turnoff)\s+([^\s()]+)", expression, flags=re.IGNORECASE)
    return match.group(1) if match else expression


def articulated_fixture_from_expression(expression: str) -> str | None:
    match = re.search(r"\b([a-z0-9_]+_\d+)_(?:top|middle|bottom)_region\b", expression, flags=re.IGNORECASE)
    return match.group(1) if match else None


def remove_object_instance(text: str, object_id: str) -> str:
    declarations = parse_typed_declarations(section_body(text, "objects", "obj_of_interest"))
    declarations.pop(object_id, None)
    text = base.replace_section(text, "objects", "obj_of_interest", render_typed_section("objects", declarations))
    kept = [
        expr
        for expr in init_expressions(section_body(text, "init", "goal"))
        if not re.search(rf"\b{re.escape(object_id)}\b", expr)
    ]
    return base.replace_section(text, "init", "goal", block("init", [f"    {expr}" for expr in kept]))


def remove_fixture_instance(text: str, fixture_id: str) -> str:
    declarations = parse_typed_declarations(section_body(text, "fixtures", "objects"))
    declarations.pop(fixture_id, None)
    text = base.replace_section(text, "fixtures", "objects", render_typed_section("fixtures", declarations))
    chunks = [
        chunk
        for chunk in split_region_chunks(section_body(text, "regions", "fixtures"))
        if region_key(chunk)[1] != fixture_id
    ]
    text = base.replace_section(text, "regions", "fixtures", block("regions", chunks))
    kept = [
        expr
        for expr in init_expressions(section_body(text, "init", "goal"))
        if not re.search(rf"\b{re.escape(fixture_id)}\b", expr)
    ]
    return base.replace_section(text, "init", "goal", block("init", [f"    {expr}" for expr in kept]))


def with_blockers_removed(
    transform: Callable[[str], str],
    *,
    objects: tuple[str, ...] = (),
    fixtures: tuple[str, ...] = (),
) -> Callable[[str], str]:
    def wrapped(text: str) -> str:
        output = transform(text)
        for object_id in objects:
            output = remove_object_instance(output, object_id)
        for fixture_id in fixtures:
            output = remove_fixture_instance(output, fixture_id)
        return output

    return wrapped


def replace_object_identity(text: str, old_id: str, new_id: str, new_type: str) -> str:
    """Replace one manipuland while preserving the rest of the source scene."""
    if old_id == new_id:
        return text
    declarations = parse_typed_declarations(section_body(text, "objects", "obj_of_interest"))
    if old_id not in declarations:
        raise ValueError(f"source object is missing: {old_id}")
    # A common source scene may already contain cream_cheese_1.  Remove that
    # distractor first, then put the instructed instance at the learned source
    # manipuland pose so the language has one unambiguous referent.
    if new_id in declarations:
        text = remove_object_instance(text, new_id)
        declarations = parse_typed_declarations(section_body(text, "objects", "obj_of_interest"))
    replaced: OrderedDict[str, str] = OrderedDict()
    for name, kind in declarations.items():
        if name == old_id:
            replaced[new_id] = new_type
        else:
            replaced[name] = kind
    text = base.replace_section(text, "objects", "obj_of_interest", render_typed_section("objects", replaced))
    expressions = [
        re.sub(rf"\b{re.escape(old_id)}\b", new_id, expr)
        for expr in init_expressions(section_body(text, "init", "goal"))
    ]
    return base.replace_section(text, "init", "goal", block("init", [f"    {expr}" for expr in expressions]))


def clean_scene(
    regions: list[str],
    fixtures: list[str],
    objects: list[str],
    init: list[str],
) -> Callable[[str], str]:
    """Merge changed entities into the original context.

    The original source scene is the default.  Supplied regions, fixtures,
    objects, and init predicates override matching entities, but unrelated
    context remains.  Individual blockers are removed explicitly with
    ``with_blockers_removed`` only when a relocated target overlaps them or
    they lie in the manipulation corridor.
    """

    def transform(text: str) -> str:
        source_regions = OrderedDict(
            (region_key(chunk), chunk)
            for chunk in split_region_chunks(section_body(text, "regions", "fixtures"))
        )
        for chunk in regions:
            source_regions[region_key(chunk)] = chunk
        text = base.replace_section(text, "regions", "fixtures", block("regions", list(source_regions.values())))

        source_fixtures = parse_typed_declarations(section_body(text, "fixtures", "objects"))
        source_fixtures.update(parse_typed_declarations("\n".join(fixtures)))
        text = base.replace_section(text, "fixtures", "objects", render_typed_section("fixtures", source_fixtures))

        source_objects = parse_typed_declarations(section_body(text, "objects", "obj_of_interest"))
        source_objects.update(parse_typed_declarations("\n".join(objects)))
        text = base.replace_section(text, "objects", "obj_of_interest", render_typed_section("objects", source_objects))

        source_init = init_expressions(section_body(text, "init", "goal"))
        supplied_init = [value.strip() for value in init]
        supplied_subjects = {init_subject(value) for value in supplied_init}
        articulated = {
            value
            for value in (articulated_fixture_from_expression(expr) for expr in supplied_init)
            if value
        }
        kept: list[str] = []
        for expr in source_init:
            if init_subject(expr) in supplied_subjects:
                continue
            fixture = articulated_fixture_from_expression(expr)
            if fixture and fixture in articulated and re.match(r"\((?:Open|Close)\b", expr, flags=re.IGNORECASE):
                continue
            kept.append(expr)
        merged_init = kept + supplied_init
        return base.replace_section(text, "init", "goal", block("init", [f"    {expr}" for expr in merged_init]))

    return transform


def mk_spec(
    task_id: str,
    family: str,
    language: str,
    source_bddl: Path,
    source_init: Path,
    source_suite: str,
    source_task_id: int | None,
    goal_atom: str,
    goal_bddl: str,
    interest: list[str],
    plan: list[dict],
    masks: list[base.MaskSelector],
    transform: Callable[[str], str],
    varied: list[str],
    fixed: list[str],
    critical: list[str],
    physical_group: str,
    notes: list[str] | None = None,
) -> base.Spec:
    return base.Spec(
        task_id=task_id,
        family=family,
        language=language,
        source_bddl=source_bddl,
        source_init=source_init,
        source_instruction=base.parse_language(source_bddl),
        source_suite=source_suite,
        source_task_id=source_task_id,
        goal_atom=goal_atom,
        goal_bddl=goal_bddl,
        objects_of_interest=interest,
        action_plan=plan,
        masks=masks,
        transform=transform,
        varied=varied,
        held_fixed=fixed,
        critical_objects=critical,
        physical_group=physical_group,
        notes=list(notes or []),
    )


def exact_plate_specs(start: int) -> list[base.Spec]:
    specs: list[base.Spec] = []
    plate_positions = {
        "left": (-0.025, -0.325, 0.025, -0.275),
        "middle": (0.075, -0.025, 0.125, 0.025),
        "right": (-0.025, 0.275, 0.025, 0.325),
    }
    plate_ids = {"left": "plate_1", "middle": "plate_3", "right": "plate_2"}
    mug_rows = [
        ("white mug", "porcelain_mug_1", "porcelain_mug", (-0.125, -0.175, -0.075, -0.125)),
        ("yellow and white mug", "white_yellow_mug_1", "white_yellow_mug", (-0.075, 0.075, -0.025, 0.125)),
    ]
    idx = start
    for label, obj, obj_type, spawn in mug_rows:
        regions = [region(f"plate_{side}_region", "living_room_table", xy) for side, xy in plate_positions.items()]
        regions.append(region(f"{obj_type}_init_region", "living_room_table", spawn, 0.0))
        transform = clean_scene(
            regions,
            ["living_room_table - living_room_table"],
            [f"{obj} - {obj_type}", "plate_1 plate_2 plate_3 - plate"],
            [
                "(On plate_1 living_room_table_plate_left_region)",
                "(On plate_3 living_room_table_plate_middle_region)",
                "(On plate_2 living_room_table_plate_right_region)",
                f"(On {obj} living_room_table_{obj_type}_init_region)",
            ],
        )
        for side in ("left", "middle", "right"):
            plate = plate_ids[side]
            language = f"Put the {label} on the {side} plate."
            blockers: tuple[str, ...] = ()
            blocker_note: list[str] = []
            if obj == "porcelain_mug_1" and side == "right":
                blockers = ("white_yellow_mug_1",)
                blocker_note = [
                    "The yellow-and-white mug is removed because it lies in the white-mug-to-right-plate corridor (the ANLG_012 collision)."
                ]
            elif obj == "white_yellow_mug_1" and side == "left":
                blockers = ("porcelain_mug_1",)
                blocker_note = [
                    "The white mug is removed because it lies in the yellow-and-white-mug-to-left-plate corridor."
                ]
            specs.append(
                mk_spec(
                    f"ANLGX_{idx:03d}",
                    "E1_clean_exact_instance_three_targets",
                    language,
                    SCENE5,
                    SCENE5_INIT,
                    "libero_10",
                    104,
                    f"on({obj}, {plate})",
                    f"(On {obj} {plate})",
                    [obj, plate],
                    base.pick_place(obj, plate, 104, language),
                    [
                        base.selector("manipulated_object", "body_prefix", obj, "green"),
                        base.selector("goal_target", "body_prefix", plate, "yellow"),
                    ],
                    with_blockers_removed(transform, objects=blockers),
                    [f"bind the learned mug-to-plate relation to the exact {side} instance among three plates"],
                    ["mug identity", "single On predicate", "three target plate poses"],
                    [obj, "plate_1", "plate_2", "plate_3"],
                    f"context_three_plates_{obj_type}" + (f"_blocker_removed_{side}" if blockers else ""),
                    [
                        "Nonblocking source-scene mugs remain; repeated plates remain because exact-instance selection is the analogy variable.",
                        *blocker_note,
                    ],
                )
            )
            idx += 1

    # Black bowl to one of three plates, using the same donor left/middle/right slots.
    regions = [region(f"plate_{side}_region", "main_table", xy) for side, xy in plate_positions.items()]
    regions.append(region("akita_black_bowl_region", "main_table", (-0.10, -0.01, -0.08, 0.01)))
    transform = clean_scene(
        regions,
        ["main_table - table"],
        ["akita_black_bowl_1 - akita_black_bowl", "plate_1 plate_2 plate_3 - plate"],
        [
            "(On akita_black_bowl_1 main_table_akita_black_bowl_region)",
            "(On plate_1 main_table_plate_left_region)",
            "(On plate_3 main_table_plate_middle_region)",
            "(On plate_2 main_table_plate_right_region)",
        ],
    )
    for side in ("left", "middle", "right"):
        plate = plate_ids[side]
        language = f"Put the black bowl on the {side} plate."
        specs.append(
            mk_spec(
                f"ANLGX_{idx:03d}", "E1_clean_exact_instance_three_targets", language,
                GOAL_BOWL_PLATE, GOAL_BOWL_PLATE_INIT, "libero_goal", 1,
                f"on(akita_black_bowl_1, {plate})", f"(On akita_black_bowl_1 {plate})",
                ["akita_black_bowl_1", plate], base.pick_place("akita_black_bowl_1", plate, 1, language),
                [base.selector("manipulated_object", "body_prefix", "akita_black_bowl_1", "green"), base.selector("goal_target", "body_prefix", plate, "yellow")],
                with_blockers_removed(transform, fixtures=("wooden_cabinet_1",)),
                [f"select the exact {side} plate among three otherwise identical targets"],
                ["black bowl identity", "learned On relation", "clean scene"],
                ["akita_black_bowl_1", "plate_1", "plate_2", "plate_3"],
                "context_three_plates_black_bowl",
                ["The wooden cabinet is removed because the added left plate overlaps its source pose."],
            )
        )
        idx += 1

    # Cream cheese to one of three same-type black bowls.
    bowl_positions = {
        "left": (0.05, -0.30, 0.07, -0.28),
        "middle": (0.05, -0.01, 0.07, 0.01),
        "right": (0.05, 0.28, 0.07, 0.30),
    }
    bowl_ids = {"left": "akita_black_bowl_1", "middle": "akita_black_bowl_2", "right": "akita_black_bowl_3"}
    regions = [region(f"bowl_{side}_region", "main_table", xy) for side, xy in bowl_positions.items()]
    regions.append(region("cream_cheese_region", "main_table", (-0.06, 0.12, -0.04, 0.14)))
    transform = clean_scene(
        regions,
        ["main_table - table"],
        ["akita_black_bowl_1 akita_black_bowl_2 akita_black_bowl_3 - akita_black_bowl", "cream_cheese_1 - cream_cheese"],
        [
            "(On akita_black_bowl_1 main_table_bowl_left_region)",
            "(On akita_black_bowl_2 main_table_bowl_middle_region)",
            "(On akita_black_bowl_3 main_table_bowl_right_region)",
            "(On cream_cheese_1 main_table_cream_cheese_region)",
        ],
    )
    for side in ("left", "middle", "right"):
        bowl = bowl_ids[side]
        language = f"Put the cream cheese on the {side} black bowl."
        specs.append(
            mk_spec(
                f"ANLGX_{idx:03d}", "E1_clean_exact_instance_three_targets", language,
                GOAL_CREAM_BOWL, GOAL_CREAM_BOWL_INIT, "libero_goal", 4,
                f"on(cream_cheese_1, {bowl})", f"(On cream_cheese_1 {bowl})",
                ["cream_cheese_1", bowl], base.pick_place("cream_cheese_1", bowl, 4, language),
                [base.selector("manipulated_object", "body_prefix", "cream_cheese_1", "green"), base.selector("goal_target", "body_prefix", bowl, "yellow")],
                with_blockers_removed(transform, objects=("plate_1",), fixtures=("wooden_cabinet_1",)),
                [f"select the exact {side} bowl among three otherwise identical receptacles"],
                ["cream-cheese identity", "learned On relation", "clean scene"],
                ["cream_cheese_1", "akita_black_bowl_1", "akita_black_bowl_2", "akita_black_bowl_3"],
                "context_three_bowls_cream_cheese",
                ["The source plate and cabinet are removed because they overlap the added middle/left bowl targets."],
            )
        )
        idx += 1
    assert idx == start + 12
    return specs


def sibling_specs(start: int) -> list[base.Spec]:
    specs: list[base.Spec] = []
    idx = start

    # Desk-caddy sibling compartments.  The irrelevant mug is removed.
    caddy_regions = [
        region("desk_caddy_init_region", "study_table", (-0.21, -0.15, -0.19, -0.13), 3.141592653589793),
        region("black_book_init_region", "study_table", (-0.025, 0.125, 0.025, 0.175), -1.178097245096),
        region("right_contain_region", "desk_caddy_1"),
        region("left_contain_region", "desk_caddy_1"),
        region("back_contain_region", "desk_caddy_1"),
        region("front_contain_region", "desk_caddy_1"),
    ]
    caddy_transform = clean_scene(
        caddy_regions,
        ["study_table - study_table", "desk_caddy_1 - desk_caddy"],
        ["black_book_1 - black_book"],
        ["(On desk_caddy_1 study_table_desk_caddy_init_region)", "(On black_book_1 study_table_black_book_init_region)"],
    )
    for compartment in ("front", "left", "right"):
        target = f"desk_caddy_1_{compartment}_contain_region"
        language = f"Put the book in the {compartment} compartment of the caddy."
        specs.append(
            mk_spec(
                f"ANLGX_{idx:03d}", "E2_sibling_part_or_compartment", language,
                STUDY1, STUDY1_INIT, "libero_10", 105,
                f"in(black_book_1, {target})", f"(In black_book_1 {target})",
                ["black_book_1", target], base.pick_place("black_book_1", target, 105, language),
                [base.selector("manipulated_object", "body_prefix", "black_book_1", "green"), base.selector("goal_target", "body_prefix", "desk_caddy_1", "yellow")],
                caddy_transform,
                [f"transfer the learned back-compartment insertion to the {compartment} sibling compartment"],
                ["book and caddy identity", "caddy pose", "single In predicate"],
                ["black_book_1"], "clean_caddy_sibling_compartments",
                ["The whole caddy is the visible destination mask because its local compartments are sites of one fixture body."],
            )
        )
        idx += 1

    def drawer_scene(
        table: str,
        table_type: str,
        fixture: str,
        fixture_type: str,
        fixture_xy: tuple[float, float, float, float],
        fixture_yaw: float,
        slot: str,
        mode: str,
        source_plate: bool = False,
    ) -> Callable[[str], str]:
        prefix = "kitchen_table" if table == "kitchen_table" else "main_table"
        regs = [region("cabinet_region", table, fixture_xy, fixture_yaw)]
        if mode in {"insert", "extract"}:
            bowl_xy = (0.005, -0.075, 0.055, -0.025) if table == "kitchen_table" else (-0.10, -0.01, -0.08, 0.01)
            regs.append(region("bowl_region", table, bowl_xy, 0.0))
        if source_plate:
            regs.append(region("plate_region", table, (0.05, 0.19, 0.07, 0.21), 0.0))
        regs.extend(region(f"{part}_region", f"{fixture}_1") for part in ("top", "middle", "bottom"))
        regs.append(region("top_side", f"{fixture}_1"))
        fixtures = [f"{table} - {table_type}", f"{fixture}_1 - {fixture_type}"]
        objects: list[str] = []
        init = [f"(On {fixture}_1 {prefix}_cabinet_region)"]
        if mode == "insert":
            objects = ["akita_black_bowl_1 - akita_black_bowl"]
            init += [f"(On akita_black_bowl_1 {prefix}_bowl_region)", f"(Open {fixture}_1_{slot}_region)"]
        elif mode == "extract":
            objects = ["akita_black_bowl_1 - akita_black_bowl", "plate_1 - plate"]
            init += [f"(On plate_1 {prefix}_plate_region)", f"(In akita_black_bowl_1 {fixture}_1_{slot}_region)", f"(Open {fixture}_1_{slot}_region)"]
        elif mode == "close":
            init.append(f"(Open {fixture}_1_{slot}_region)")
        return clean_scene(regs, fixtures, objects, init)

    # Insertion into missing white-cabinet siblings.
    for slot in ("top", "middle"):
        fixture = "white_cabinet_1"
        target = f"{fixture}_{slot}_region"
        language = f"Put the black bowl in the {slot} drawer of the white cabinet."
        transform = drawer_scene("kitchen_table", "kitchen_table", "white_cabinet", "white_cabinet", (-0.01, 0.29, 0.01, 0.31), 0.0, slot, "insert")
        specs.append(
            mk_spec(
                f"ANLGX_{idx:03d}", "E2_sibling_part_or_compartment", language,
                KITCHEN4, KITCHEN4_INIT, "libero_10", 103,
                f"in(akita_black_bowl_1, {target})", f"(In akita_black_bowl_1 {target})",
                ["akita_black_bowl_1", target], base.pick_place("akita_black_bowl_1", target, 103, language),
                [base.selector("manipulated_object", "body_prefix", "akita_black_bowl_1", "green"), base.selector("goal_target", "drawer_part", f"white_cabinet_1:{slot}", "yellow")],
                transform, [f"transfer bottom-drawer insertion to the {slot} sibling"],
                ["white cabinet pose/type", "bowl identity", "target drawer initialized open"],
                ["akita_black_bowl_1"], f"white_insert_{slot}",
            )
        )
        idx += 1

    # Insertion into missing wooden-cabinet siblings.
    for slot in ("middle", "bottom"):
        target = f"wooden_cabinet_1_{slot}_region"
        language = f"Put the black bowl in the {slot} drawer of the wooden cabinet."
        transform = drawer_scene("main_table", "table", "wooden_cabinet", "wooden_cabinet", (0.02, -0.25, 0.04, -0.23), 3.141592653589793, slot, "insert")
        specs.append(
            mk_spec(
                f"ANLGX_{idx:03d}", "E2_sibling_part_or_compartment", language,
                GOAL_INSERT_TOP, GOAL_INSERT_TOP_INIT, "libero_goal", 3,
                f"in(akita_black_bowl_1, {target})", f"(In akita_black_bowl_1 {target})",
                ["akita_black_bowl_1", target], base.pick_place("akita_black_bowl_1", target, 3, language),
                [base.selector("manipulated_object", "body_prefix", "akita_black_bowl_1", "green"), base.selector("goal_target", "drawer_part", f"wooden_cabinet_1:{slot}", "yellow")],
                transform, [f"transfer top-drawer insertion to the {slot} sibling"],
                ["wooden cabinet pose/type", "bowl identity", "target drawer initialized open"],
                ["akita_black_bowl_1"], f"wooden_insert_{slot}",
            )
        )
        idx += 1

    # Open missing wooden-cabinet siblings.
    for slot in ("top", "bottom"):
        target = f"wooden_cabinet_1_{slot}_region"
        language = f"Open the {slot} drawer of the wooden cabinet."
        transform = drawer_scene("main_table", "table", "wooden_cabinet", "wooden_cabinet", (0.02, -0.25, 0.04, -0.23), 3.141592653589793, slot, "open")
        specs.append(
            mk_spec(
                f"ANLGX_{idx:03d}", "E2_sibling_part_or_compartment", language,
                GOAL_OPEN_MIDDLE, GOAL_OPEN_MIDDLE_INIT, "libero_goal", 10,
                f"open({target})", f"(Open {target})", [target],
                [base.action("open", target, target, 10, language)],
                [base.selector("interaction_target", "drawer_part", f"wooden_cabinet_1:{slot}", "green")],
                transform, [f"transfer middle-drawer opening to the {slot} sibling"],
                ["wooden cabinet pose/type", "single Open predicate", "no movable clutter"],
                [], "wooden_open_clean",
            )
        )
        idx += 1

    # Close missing white-cabinet siblings.
    for slot in ("top", "middle"):
        target = f"white_cabinet_1_{slot}_region"
        language = f"Close the {slot} drawer of the white cabinet."
        transform = drawer_scene("kitchen_table", "kitchen_table", "white_cabinet", "white_cabinet", (-0.01, 0.29, 0.01, 0.31), 0.0, slot, "close")
        specs.append(
            mk_spec(
                f"ANLGX_{idx:03d}", "E2_sibling_part_or_compartment", language,
                KITCHEN4, KITCHEN4_INIT, "libero_10", 103,
                f"close({target})", f"(Close {target})", [target],
                [base.action("close", target, target, 103, language)],
                [base.selector("interaction_target", "drawer_part", f"white_cabinet_1:{slot}", "green")],
                transform, [f"transfer learned bottom-drawer closing to the {slot} sibling"],
                ["white cabinet pose/type", "target initialized open", "no movable clutter"],
                [], f"white_close_{slot}",
            )
        )
        idx += 1

    # Pick the bowl out of a sibling drawer and retain the learned bowl-to-plate goal.
    for slot in ("middle", "bottom"):
        language = f"Pick up the black bowl in the {slot} drawer of the wooden cabinet and place it on the plate."
        transform = drawer_scene("main_table", "table", "wooden_cabinet", "wooden_cabinet", (0.02, -0.28, 0.04, -0.26), 2.692793703077, slot, "extract", source_plate=True)
        specs.append(
            mk_spec(
                f"ANLGX_{idx:03d}", "E2_sibling_part_or_compartment", language,
                SPATIAL_DRAWER, SPATIAL_DRAWER_INIT, "libero_spatial", None,
                "on(akita_black_bowl_1, plate_1)", "(On akita_black_bowl_1 plate_1)",
                ["akita_black_bowl_1", "plate_1"], base.pick_place("akita_black_bowl_1", "plate_1", None, language),
                [base.selector("manipulated_object", "body_prefix", "akita_black_bowl_1", "green"), base.selector("goal_target", "body_prefix", "plate_1", "yellow")],
                transform, [f"move the learned bowl start from the top drawer to the {slot} sibling"],
                ["wooden cabinet and plate pose", "bowl-to-plate goal", "target drawer initialized open"],
                ["plate_1"], f"wooden_extract_{slot}",
                ["Init gate: after settling, the bowl must still satisfy In(bowl, instructed drawer); drawer-contained rotation is allowed."],
            )
        )
        idx += 1
    assert idx == start + 13
    return specs


def fixture_pose_specs(start: int) -> list[base.Spec]:
    specs: list[base.Spec] = []
    idx = start
    stove_poses = {
        "spatial donor position": (-0.42, -0.15, -0.40, -0.13),
        "LIBERO-10 Scene 3 donor position": (-0.21, 0.19, -0.19, 0.21),
        "LIBERO-10 Scene 8 donor position": (-0.21, -0.21, -0.19, -0.19),
    }

    def stove_transform(
        pose: tuple[float, float, float, float],
        mode: str,
        table: str = "main_table",
    ) -> Callable[[str], str]:
        table_type = "table" if table == "main_table" else "kitchen_table"
        regs = [region("stove_region", table, pose, 0.0), region("cook_region", "flat_stove_1")]
        objects: list[str] = []
        init = [f"(On flat_stove_1 {table}_stove_region)"]
        if mode == "push":
            center_x = (pose[0] + pose[2]) / 2.0
            center_y = (pose[1] + pose[3]) / 2.0
            regs += [
                region("plate_region", table, (0.04, -0.03, 0.06, -0.01), 0.0),
                region("stove_front_region", table, (center_x + 0.32, center_y - 0.04, center_x + 0.40, center_y + 0.04), 0.0),
            ]
            objects = ["plate_1 - plate"]
            init.append(f"(On plate_1 {table}_plate_region)")
        elif mode == "bowl_on":
            regs.append(region("bowl_region", table, (-0.10, -0.01, -0.08, 0.01), 0.0))
            objects = ["akita_black_bowl_1 - akita_black_bowl"]
            init.append(f"(On akita_black_bowl_1 {table}_bowl_region)")
        elif mode == "bowl_from":
            regs.append(region("plate_region", table, (0.05, 0.19, 0.07, 0.21), 0.0))
            objects = ["akita_black_bowl_1 - akita_black_bowl", "plate_1 - plate"]
            init += [f"(On akita_black_bowl_1 flat_stove_1_cook_region)", f"(On plate_1 {table}_plate_region)"]
        elif mode == "moka_on":
            regs.append(region("moka_region", table, (0.025, -0.025, 0.075, 0.025), 0.0))
            objects = ["moka_pot_1 - moka_pot"]
            init.append(f"(On moka_pot_1 {table}_moka_region)")
        return clean_scene(regs, [f"{table} - {table_type}", "flat_stove_1 - flat_stove"], objects, init)

    def goal_stove_context_transform(donor: str, pose: tuple[float, float, float, float], mode: str) -> tuple[Callable[[str], str], list[str]]:
        fixtures: tuple[str, ...] = ()
        notes: list[str] = []
        if donor == "spatial donor position":
            fixtures = ("wine_rack_1", "wooden_cabinet_1") if mode == "push" else ("wine_rack_1",)
        elif donor == "LIBERO-10 Scene 8 donor position":
            fixtures = ("wine_rack_1", "wooden_cabinet_1")
        if "wine_rack_1" in fixtures:
            notes.append("The source wine rack is removed because the relocated stove overlaps its footprint.")
        if "wooden_cabinet_1" in fixtures:
            notes.append("The source cabinet is removed because it blocks the relocated stove or its translated front corridor.")
        return with_blockers_removed(stove_transform(pose, mode), fixtures=fixtures), notes

    for donor, pose in stove_poses.items():
        language = f"Turn on the stove at the {donor}."
        task_transform, blocker_notes = goal_stove_context_transform(donor, pose, "turn")
        specs.append(
            mk_spec(
                f"ANLGX_{idx:03d}", "E3_reference_fixture_pose_transfer", language,
                GOAL_TURN_STOVE, GOAL_TURN_STOVE_INIT, "libero_goal", 7,
                "turnon(flat_stove_1)", "(Turnon flat_stove_1)", ["flat_stove_1"],
                [base.action("turn_on", "flat_stove_1", "flat_stove_1", 7, language)],
                [base.selector("interaction_target", "body_prefix", "flat_stove_1", "green")],
                task_transform, [f"move the stove to the {donor}, a pose used in original LIBERO-40"],
                ["stove identity/yaw", "single Turnon predicate", "nonblocking source context"], [],
                f"stove_turn_{idx}",
                blocker_notes,
            )
        )
        idx += 1

    for donor, pose in stove_poses.items():
        center_x = (pose[0] + pose[2]) / 2.0
        center_y = (pose[1] + pose[3]) / 2.0
        front = (center_x + 0.32, center_y - 0.04, center_x + 0.40, center_y + 0.04)
        language = f"Push the plate to the front of the stove at the {donor}."
        task_transform, blocker_notes = goal_stove_context_transform(donor, pose, "push")
        specs.append(
            mk_spec(
                f"ANLGX_{idx:03d}", "E3_reference_fixture_pose_transfer", language,
                GOAL_PUSH_STOVE, GOAL_PUSH_STOVE_INIT, "libero_goal", 6,
                "on(plate_1, main_table_stove_front_region)", "(On plate_1 main_table_stove_front_region)",
                ["plate_1", "main_table_stove_front_region"],
                [base.action("approach", "plate_1", "plate_1", 6, language), base.action("push", "plate_1", "main_table_stove_front_region", 6, language)],
                [base.selector("manipulated_object", "body_prefix", "plate_1", "green"), base.selector("goal_target", "table_region", "main_table_stove_front_region", "yellow")],
                task_transform,
                [f"move the stove to the {donor}", f"translate its front region to {front}"],
                ["plate identity/start", "stove yaw", "reference-relative front relation"],
                ["plate_1"], f"stove_push_{idx}",
                ["The placement mask is projected from the current BDDL front region, never copied from the source absolute coordinates.", *blocker_notes],
            )
        )
        idx += 1

    for donor, pose in stove_poses.items():
        language = f"Put the black bowl on the stove at the {donor}."
        task_transform, blocker_notes = goal_stove_context_transform(donor, pose, "bowl_on")
        specs.append(
            mk_spec(
                f"ANLGX_{idx:03d}", "E3_reference_fixture_pose_transfer", language,
                GOAL_BOWL_STOVE, GOAL_BOWL_STOVE_INIT, "libero_goal", 8,
                "on(akita_black_bowl_1, flat_stove_1_cook_region)", "(On akita_black_bowl_1 flat_stove_1_cook_region)",
                ["akita_black_bowl_1", "flat_stove_1_cook_region"], base.pick_place("akita_black_bowl_1", "flat_stove_1_cook_region", 8, language),
                [base.selector("manipulated_object", "body_prefix", "akita_black_bowl_1", "green"), base.selector("goal_target", "body_prefix", "flat_stove_1", "yellow")],
                task_transform, [f"move the stove to the {donor}"],
                ["bowl identity/start", "stove identity/yaw", "single On relation"],
                ["akita_black_bowl_1"], f"stove_bowl_on_{idx}", blocker_notes,
            )
        )
        idx += 1

    bowl_from_poses = {
        "Goal donor position": (-0.42, 0.20, -0.40, 0.22),
        "LIBERO-10 Scene 3 donor position": (-0.21, 0.19, -0.19, 0.21),
        "LIBERO-10 Scene 8 donor position": (-0.21, -0.21, -0.19, -0.19),
    }
    for donor, pose in bowl_from_poses.items():
        if donor == "LIBERO-10 Scene 8 donor position":
            # Rejected by the simulator gate: repeated attempts could not
            # produce one stable initial state with the bowl already on this
            # relocated stove. The corresponding bowl-to-stove goal task is
            # stable and remains in the pool.
            continue
        language = f"Pick up the black bowl on the stove at the {donor} and place it on the plate."
        extract_transform = stove_transform(pose, "bowl_from")
        extract_notes: list[str] = []
        if donor == "LIBERO-10 Scene 8 donor position":
            extract_transform = with_blockers_removed(extract_transform, fixtures=("wooden_cabinet_1",))
            extract_notes.append("The source cabinet is removed because it overlaps the Scene-8 stove footprint.")
        specs.append(
            mk_spec(
                f"ANLGX_{idx:03d}", "E3_reference_fixture_pose_transfer", language,
                SPATIAL_STOVE, SPATIAL_STOVE_INIT, "libero_spatial", None,
                "on(akita_black_bowl_1, plate_1)", "(On akita_black_bowl_1 plate_1)",
                ["akita_black_bowl_1", "plate_1"], base.pick_place("akita_black_bowl_1", "plate_1", None, language),
                [base.selector("manipulated_object", "body_prefix", "akita_black_bowl_1", "green"), base.selector("goal_target", "body_prefix", "plate_1", "yellow")],
                extract_transform, [f"move the stove and bowl initialized on it to the {donor}"],
                ["plate pose", "bowl-to-plate goal", "stove identity/yaw"],
                ["akita_black_bowl_1", "plate_1"], f"stove_bowl_from_{idx}", extract_notes,
            )
        )
        idx += 1

    for donor, pose in (
        ("Goal donor position", (-0.42, 0.20, -0.40, 0.22)),
        ("Spatial donor position", (-0.42, -0.15, -0.40, -0.13)),
    ):
        language = f"Put the moka pot on the stove at the {donor}."
        specs.append(
            mk_spec(
                f"ANLGX_{idx:03d}", "E3_reference_fixture_pose_transfer", language,
                KITCHEN3, KITCHEN3_INIT, "libero_10", 101,
                "on(moka_pot_1, flat_stove_1_cook_region)", "(On moka_pot_1 flat_stove_1_cook_region)",
                ["moka_pot_1", "flat_stove_1_cook_region"], base.pick_place("moka_pot_1", "flat_stove_1_cook_region", 101, language),
                [base.selector("manipulated_object", "body_prefix", "moka_pot_1", "green"), base.selector("goal_target", "body_prefix", "flat_stove_1", "yellow")],
                stove_transform(pose, "moka_on", table="kitchen_table"), [f"move the stove to the {donor}"],
                ["moka-pot identity/start", "single On relation", "nonblocking source context"],
                ["moka_pot_1"], f"stove_moka_{idx}",
            )
        )
        idx += 1

    # Same articulated fixture and drawer identity at the original white-cabinet donor pose.
    cabinet_pose = (-0.01, 0.29, 0.01, 0.31)
    cabinet_transform = clean_scene(
        [
            region("cabinet_region", "main_table", cabinet_pose, 0.0),
            region("top_region", "wooden_cabinet_1"),
            region("middle_region", "wooden_cabinet_1"),
            region("bottom_region", "wooden_cabinet_1"),
            region("top_side", "wooden_cabinet_1"),
        ],
        ["main_table - table", "wooden_cabinet_1 - wooden_cabinet"], [],
        ["(On wooden_cabinet_1 main_table_cabinet_region)"],
    )
    for slot, source_bddl, source_init, source_id in (
        ("middle", GOAL_OPEN_MIDDLE, GOAL_OPEN_MIDDLE_INIT, 10),
        ("top", GOAL_INSERT_TOP, GOAL_INSERT_TOP_INIT, 3),
    ):
        target = f"wooden_cabinet_1_{slot}_region"
        language = f"Open the {slot} drawer of the wooden cabinet at the white-cabinet donor position."
        specs.append(
            mk_spec(
                f"ANLGX_{idx:03d}", "E3_reference_fixture_pose_transfer", language,
                source_bddl, source_init, "libero_goal", source_id,
                f"open({target})", f"(Open {target})", [target],
                [base.action("open", target, target, source_id, language)],
                [base.selector("interaction_target", "drawer_part", f"wooden_cabinet_1:{slot}", "green")],
                cabinet_transform,
                ["move the wooden cabinet to the exact LIBERO-10 white-cabinet pose and keep its front arm-facing"],
                ["wooden cabinet type", f"{slot} drawer binding", "single Open predicate", "no movable clutter"],
                [], "relocated_wooden_open_clean",
            )
        )
        idx += 1
    assert idx == start + 15
    return specs


def receptacle_support_specs(start: int) -> list[base.Spec]:
    specs: list[base.Spec] = []
    idx = start

    # Two caddy relocations use original book/mug interaction slots as finite donors.
    caddy_rows = [
        ("book-slot donor position", (-0.025, 0.125, 0.025, 0.175), (-0.21, -0.15, -0.19, -0.13)),
        ("mug-slot donor position", (0.075, -0.025, 0.125, 0.025), (-0.025, 0.125, 0.025, 0.175)),
    ]
    for donor, caddy_xy, book_xy in caddy_rows:
        transform = clean_scene(
            [
                region("desk_caddy_init_region", "study_table", caddy_xy, 3.141592653589793),
                region("black_book_init_region", "study_table", book_xy, -1.178097245096),
                region("right_contain_region", "desk_caddy_1"), region("left_contain_region", "desk_caddy_1"),
                region("back_contain_region", "desk_caddy_1"), region("front_contain_region", "desk_caddy_1"),
            ],
            ["study_table - study_table", "desk_caddy_1 - desk_caddy"], ["black_book_1 - black_book"],
            ["(On desk_caddy_1 study_table_desk_caddy_init_region)", "(On black_book_1 study_table_black_book_init_region)"],
        )
        blocker_notes: list[str] = []
        if donor == "mug-slot donor position":
            transform = with_blockers_removed(transform, objects=("white_yellow_mug_1",))
            blocker_notes.append("The source mug is removed because the relocated caddy occupies its exact pose.")
        language = f"Put the book in the back compartment of the caddy at the {donor}."
        target = "desk_caddy_1_back_contain_region"
        specs.append(
            mk_spec(
                f"ANLGX_{idx:03d}", "E4_clean_receptacle_or_support_transfer", language,
                STUDY1, STUDY1_INIT, "libero_10", 105,
                f"in(black_book_1, {target})", f"(In black_book_1 {target})", ["black_book_1", target],
                base.pick_place("black_book_1", target, 105, language),
                [base.selector("manipulated_object", "body_prefix", "black_book_1", "green"), base.selector("goal_target", "body_prefix", "desk_caddy_1", "yellow")],
                transform, [f"move the caddy to the original {donor}; move the book to another original interaction slot"],
                ["book/caddy identities", "back compartment", "single In predicate", "nonblocking source context"],
                ["black_book_1"], f"caddy_reloc_{idx}", blocker_notes,
            )
        )
        idx += 1

    # Microwave at two learned fixture positions: insertion and atomic closing.
    for donor, microwave_xy in (
        ("Scene 3 fixture position", (-0.21, 0.19, -0.19, 0.21)),
        ("Scene 8 fixture position", (-0.21, -0.21, -0.19, -0.19)),
    ):
        transform = clean_scene(
            [
                region("microwave_init_region", "kitchen_table", microwave_xy, 0.0),
                region("white_yellow_mug_init_region", "kitchen_table", (-0.025, -0.025, 0.025, 0.025), 0.0),
                region("top_side", "microwave_1"), region("heating_region", "microwave_1"),
            ],
            ["kitchen_table - kitchen_table", "microwave_1 - microwave"], ["white_yellow_mug_1 - white_yellow_mug"],
            ["(On white_yellow_mug_1 kitchen_table_white_yellow_mug_init_region)", "(On microwave_1 kitchen_table_microwave_init_region)", "(Open microwave_1)"],
        )
        blocker_notes: list[str] = []
        if donor == "Scene 8 fixture position":
            transform = with_blockers_removed(transform, objects=("porcelain_mug_1",))
            blocker_notes.append("The porcelain mug is removed because the left microwave overlaps its source pose.")
        physical_group = "microwave_reloc_" + re.sub(r"[^a-z0-9]+", "_", donor.lower()).strip("_")
        language = f"Put the yellow and white mug in the microwave at the {donor}."
        target = "microwave_1_heating_region"
        specs.append(
            mk_spec(
                f"ANLGX_{idx:03d}", "E4_clean_receptacle_or_support_transfer", language,
                KITCHEN6, KITCHEN6_INIT, "libero_10", 109,
                f"in(white_yellow_mug_1, {target})", f"(In white_yellow_mug_1 {target})",
                ["white_yellow_mug_1", target], base.pick_place("white_yellow_mug_1", target, 109, language),
                [base.selector("manipulated_object", "body_prefix", "white_yellow_mug_1", "green"), base.selector("goal_target", "body_prefix", "microwave_1", "yellow")],
                transform, [f"move the microwave to the original LIBERO-10 {donor}"],
                ["mug/microwave identities", "microwave initialized open", "nonblocking source context"],
                ["white_yellow_mug_1"], physical_group, blocker_notes,
            )
        )
        idx += 1

        close_language = f"Close the microwave at the {donor}."
        specs.append(
            mk_spec(
                f"ANLGX_{idx:03d}", "E4_clean_receptacle_or_support_transfer", close_language,
                KITCHEN6, KITCHEN6_INIT, "libero_10", 109,
                "close(microwave_1)", "(Close microwave_1)", ["microwave_1"],
                [base.action("close", "microwave_1", "microwave_1", 109, close_language)],
                [base.selector("interaction_target", "body_prefix", "microwave_1", "green")],
                transform, [f"move the microwave to the original LIBERO-10 {donor} and isolate its learned close primitive"],
                ["microwave identity", "door initialized open", "nonblocking source context"],
                [], physical_group, blocker_notes,
            )
        )
        idx += 1

    # Atomic basket primitives at an original grasp slot (Scene-1 ketchup slot).
    # The alphabet-soup variant is deliberately absent: repeated simulator
    # smoke attempts produced 0 stable states for that exact combination.
    basket_xy = (-0.21, -0.17, -0.19, -0.15)
    basket_rows = [
        ("cream cheese", "cream_cheese_1", "cream_cheese", (-0.175, 0.035, -0.125, 0.085), SCENE1, SCENE1_INIT, 107),
        ("tomato sauce", "tomato_sauce_1", "tomato_sauce", (-0.125, 0.025, -0.075, 0.075), SCENE2, SCENE2_INIT, 108),
        ("butter", "butter_1", "butter", (0.025, 0.025, 0.075, 0.075), SCENE2, SCENE2_INIT, 108),
    ]
    for label, obj, obj_type, obj_xy, source_bddl, source_init, source_id in basket_rows:
        transform = clean_scene(
            [region("basket_init_region", "living_room_table", basket_xy, 0.0), region(f"{obj_type}_init_region", "living_room_table", obj_xy, 0.0), region("contain_region", "basket_1")],
            ["living_room_table - living_room_table"], [f"{obj} - {obj_type}", "basket_1 - basket"],
            [f"(On {obj} living_room_table_{obj_type}_init_region)", "(On basket_1 living_room_table_basket_init_region)"],
        )
        language = f"Put the {label} in the basket at the former ketchup position."
        target = "basket_1_contain_region"
        specs.append(
            mk_spec(
                f"ANLGX_{idx:03d}", "E4_clean_receptacle_or_support_transfer", language,
                source_bddl, source_init, "libero_10", source_id,
                f"in({obj}, {target})", f"(In {obj} {target})", [obj, target],
                base.pick_place(obj, target, source_id, language),
                [base.selector("manipulated_object", "body_prefix", obj, "green"), base.selector("goal_target", "body_prefix", "basket_1", "yellow")],
                with_blockers_removed(transform, objects=("ketchup_1",)), ["move the basket to a collision-free slot occupied by a grasped object in original LIBERO-10"],
                [f"{label} identity/start", "basket identity", "single In predicate", "nonblocking source context"],
                [obj], f"basket_reloc_{obj_type}",
                ["The source ketchup is removed because the relocated basket occupies its exact init region."],
            )
        )
        idx += 1

    # Wine rack transferred to the position used by the LIBERO-10 white-cabinet scene.
    rack_transform = clean_scene(
        [
            region("wine_rack_region", "main_table", (-0.11, -0.31, -0.09, -0.29), 3.141592653589793),
            region("wine_bottle_region", "main_table", (-0.21, -0.06, -0.19, -0.04), 0.0),
            region("top_region", "wine_rack_1"),
        ],
        ["main_table - table", "wine_rack_1 - wine_rack"], ["wine_bottle_1 - wine_bottle"],
        ["(On wine_bottle_1 main_table_wine_bottle_region)", "(On wine_rack_1 main_table_wine_rack_region)"],
    )
    language = "Put the wine bottle on the rack at the LIBERO-10 rack position."
    specs.append(
        mk_spec(
            f"ANLGX_{idx:03d}", "E4_clean_receptacle_or_support_transfer", language,
            GOAL_WINE_RACK, GOAL_WINE_RACK_INIT, "libero_goal", 2,
            "on(wine_bottle_1, wine_rack_1_top_region)", "(On wine_bottle_1 wine_rack_1_top_region)",
            ["wine_bottle_1", "wine_rack_1_top_region"], base.pick_place("wine_bottle_1", "wine_rack_1_top_region", 2, language),
            [base.selector("manipulated_object", "body_prefix", "wine_bottle_1", "green"), base.selector("goal_target", "body_prefix", "wine_rack_1", "yellow")],
            with_blockers_removed(rack_transform, fixtures=("wooden_cabinet_1",)), ["move the rack from the Goal pose to the exact LIBERO-10 rack pose"],
            ["wine-bottle/rack identities", "single On relation", "nonblocking Goal-scene context"],
            ["wine_bottle_1"], "wine_rack_reloc_context",
            ["The wooden cabinet is removed because the relocated rack overlaps its source footprint."],
        )
    )
    idx += 1

    # Two learned cabinet-top placements at the articulated-fixture donor pose.
    for label, obj, obj_type, source_bddl, source_init, source_id, obj_xy in (
        ("black bowl", "akita_black_bowl_1", "akita_black_bowl", GOAL_BOWL_CABINET, GOAL_BOWL_CABINET_INIT, 9, (-0.10, -0.01, -0.08, 0.01)),
        ("wine bottle", "wine_bottle_1", "wine_bottle", GOAL_WINE_CABINET, GOAL_WINE_CABINET_INIT, 5, (-0.21, -0.06, -0.19, -0.04)),
    ):
        transform = clean_scene(
            [
                region("cabinet_region", "main_table", (-0.01, 0.29, 0.01, 0.31), 0.0),
                region("object_region", "main_table", obj_xy, 0.0),
                region("top_region", "wooden_cabinet_1"), region("middle_region", "wooden_cabinet_1"),
                region("bottom_region", "wooden_cabinet_1"), region("top_side", "wooden_cabinet_1"),
            ],
            ["main_table - table", "wooden_cabinet_1 - wooden_cabinet"], [f"{obj} - {obj_type}"],
            [f"(On {obj} main_table_object_region)", "(On wooden_cabinet_1 main_table_cabinet_region)"],
        )
        language = f"Put the {label} on top of the wooden cabinet at the white-cabinet donor position."
        target = "wooden_cabinet_1_top_side"
        specs.append(
            mk_spec(
                f"ANLGX_{idx:03d}", "E4_clean_receptacle_or_support_transfer", language,
                source_bddl, source_init, "libero_goal", source_id,
                f"on({obj}, {target})", f"(On {obj} {target})", [obj, target],
                base.pick_place(obj, target, source_id, language),
                [base.selector("manipulated_object", "body_prefix", obj, "green"), base.selector("goal_target", "body_prefix", "wooden_cabinet_1", "yellow")],
                transform, ["move the cabinet to the exact LIBERO-10 white-cabinet pose with an arm-facing yaw"],
                [f"{label} identity/start", "wooden cabinet identity", "single On relation", "nonblocking Goal-scene context"],
                [obj], f"cabinet_top_reloc_{obj_type}",
            )
        )
        idx += 1
    assert idx == start + 12
    return specs


PACKAGE_OBJECTS = [
    ("alphabet soup", "alphabet_soup_1", "alphabet_soup", 301),
    ("cream cheese", "cream_cheese_1", "cream_cheese", 302),
    ("salad dressing", "salad_dressing_1", "salad_dressing", 303),
    ("bbq sauce", "bbq_sauce_1", "bbq_sauce", 304),
    ("ketchup", "ketchup_1", "ketchup", 305),
    ("tomato sauce", "tomato_sauce_1", "tomato_sauce", 306),
    ("butter", "butter_1", "butter", 307),
    ("milk", "milk_1", "milk", 308),
    ("chocolate pudding", "chocolate_pudding_1", "chocolate_pudding", 309),
    ("orange juice", "orange_juice_1", "orange_juice", 310),
]


def package_relation_specs(start: int) -> list[base.Spec]:
    """Cross learned package grasps with compatible learned target relations."""
    specs: list[base.Spec] = []
    idx = start

    relation_rows = [
        {
            "key": "wine_rack",
            "preposition": "on",
            "target_label": "wine rack",
            "source_bddl": GOAL_WINE_RACK,
            "source_init": GOAL_WINE_RACK_INIT,
            "source_suite": "libero_goal",
            "old_id": "wine_bottle_1",
            "target": "wine_rack_1_top_region",
            "target_mask": "wine_rack_1",
            "target_mask_kind": "body_prefix",
            "predicate": "On",
            "open_drawer": False,
        },
        {
            "key": "plate",
            "preposition": "on",
            "target_label": "plate",
            "source_bddl": GOAL_BOWL_PLATE,
            "source_init": GOAL_BOWL_PLATE_INIT,
            "source_suite": "libero_goal",
            "old_id": "akita_black_bowl_1",
            "target": "plate_1",
            "target_mask": "plate_1",
            "target_mask_kind": "body_prefix",
            "predicate": "On",
            "open_drawer": False,
        },
        {
            "key": "black_bowl",
            "preposition": "on",
            "target_label": "black bowl",
            "source_bddl": GOAL_CREAM_BOWL,
            "source_init": GOAL_CREAM_BOWL_INIT,
            "source_suite": "libero_goal",
            "old_id": "cream_cheese_1",
            "target": "akita_black_bowl_1",
            "target_mask": "akita_black_bowl_1",
            "target_mask_kind": "body_prefix",
            "predicate": "On",
            "open_drawer": False,
        },
        {
            "key": "stove",
            "preposition": "on",
            "target_label": "stove",
            "source_bddl": GOAL_BOWL_STOVE,
            "source_init": GOAL_BOWL_STOVE_INIT,
            "source_suite": "libero_goal",
            "old_id": "akita_black_bowl_1",
            "target": "flat_stove_1_cook_region",
            "target_mask": "flat_stove_1",
            "target_mask_kind": "body_prefix",
            "predicate": "On",
            "open_drawer": False,
        },
        {
            "key": "cabinet_top",
            "preposition": "on top of",
            "target_label": "wooden cabinet",
            "source_bddl": GOAL_BOWL_CABINET,
            "source_init": GOAL_BOWL_CABINET_INIT,
            "source_suite": "libero_goal",
            "old_id": "akita_black_bowl_1",
            "target": "wooden_cabinet_1_top_side",
            "target_mask": "wooden_cabinet_1",
            "target_mask_kind": "body_prefix",
            "predicate": "On",
            "open_drawer": False,
        },
        {
            "key": "wooden_top_drawer",
            "preposition": "in",
            "target_label": "top drawer of the wooden cabinet",
            "source_bddl": GOAL_INSERT_TOP,
            "source_init": GOAL_INSERT_TOP_INIT,
            "source_suite": "libero_goal",
            "old_id": "akita_black_bowl_1",
            "target": "wooden_cabinet_1_top_region",
            "target_mask": "wooden_cabinet_1:top",
            "target_mask_kind": "drawer_part",
            "predicate": "In",
            "open_drawer": True,
        },
        {
            "key": "microwave",
            "preposition": "in",
            "target_label": "microwave",
            "source_bddl": KITCHEN6,
            "source_init": KITCHEN6_INIT,
            "source_suite": "libero_10",
            "old_id": "white_yellow_mug_1",
            "target": "microwave_1_heating_region",
            "target_mask": "microwave_1",
            "target_mask_kind": "body_prefix",
            "predicate": "In",
            "open_drawer": False,
        },
    ]

    for relation in relation_rows:
        for label, object_id, object_type, source_object_task_id in PACKAGE_OBJECTS:
            # This exact relation is already an original LIBERO-Goal task.
            if relation["key"] == "black_bowl" and object_id == "cream_cheese_1":
                continue

            def transform(
                text: str,
                *,
                old_id: str = str(relation["old_id"]),
                new_id: str = object_id,
                new_type: str = object_type,
                open_drawer: bool = bool(relation["open_drawer"]),
            ) -> str:
                output = replace_object_identity(text, old_id, new_id, new_type)
                if open_drawer:
                    output = base.replace_open_init(output, "wooden_cabinet_1", "top")
                return output

            target = str(relation["target"])
            predicate = str(relation["predicate"])
            language = f"Put the {label} {relation['preposition']} the {relation['target_label']}."
            goal_atom = f"{predicate.lower()}({object_id}, {target})"
            target_selector = base.selector(
                "goal_target",
                str(relation["target_mask_kind"]),
                str(relation["target_mask"]),
                "yellow",
            )
            specs.append(
                mk_spec(
                    f"ANLGX_{idx:03d}",
                    "E5_seen_object_new_relation_binding",
                    language,
                    Path(relation["source_bddl"]),
                    Path(relation["source_init"]),
                    str(relation["source_suite"]),
                    source_object_task_id,
                    goal_atom,
                    f"({predicate} {object_id} {target})",
                    [object_id, target],
                    base.pick_place(object_id, target, source_object_task_id, language),
                    [
                        base.selector("manipulated_object", "body_prefix", object_id, "green"),
                        target_selector,
                    ],
                    transform,
                    [
                        f"replace the source manipuland with {label}, whose grasp was learned in original LIBERO-Object",
                        f"apply the learned {predicate} relation to the {relation['target_label']}",
                    ],
                    [
                        "target fixture/receptacle identity and pose",
                        "source scene context except duplicate-instance removal",
                        "one semantic goal atom",
                    ],
                    [object_id],
                    f"package_relation_{relation['key']}_{object_type}",
                    [
                        f"Object-grasp evidence: original LIBERO-Object task {source_object_task_id}.",
                        "If this object already existed as a distractor, that duplicate is removed and the single instructed instance is placed at the source manipuland pose.",
                    ],
                )
            )
            idx += 1

    # Caddy back compartment is narrower; admit the eight package objects
    # whose declared horizontal radius is <= 0.025 m.  Milk and cream cheese
    # are 0.030 m and are therefore rejected before simulation.
    caddy_packages = [row for row in PACKAGE_OBJECTS if row[2] not in {"milk", "cream_cheese"}]
    for label, object_id, object_type, source_object_task_id in caddy_packages:
        def transform(
            text: str,
            *,
            new_id: str = object_id,
            new_type: str = object_type,
        ) -> str:
            return replace_object_identity(text, "black_book_1", new_id, new_type)

        target = "desk_caddy_1_back_contain_region"
        language = f"Put the {label} in the back compartment of the caddy."
        specs.append(
            mk_spec(
                f"ANLGX_{idx:03d}", "E5_seen_object_new_relation_binding", language,
                STUDY1, STUDY1_INIT, "libero_10", source_object_task_id,
                f"in({object_id}, {target})", f"(In {object_id} {target})",
                [object_id, target], base.pick_place(object_id, target, source_object_task_id, language),
                [base.selector("manipulated_object", "body_prefix", object_id, "green"), base.selector("goal_target", "body_prefix", "desk_caddy_1", "yellow")],
                transform,
                [f"replace the book with {label}, a seen grasp object that fits the caddy aperture"],
                ["caddy pose and back compartment", "source mug context", "single In predicate"],
                [object_id], f"package_relation_caddy_{object_type}",
                [f"Object-grasp evidence: original LIBERO-Object task {source_object_task_id}; compatibility gate: horizontal radius <= 0.025 m."],
            )
        )
        idx += 1

    assert idx == start + 77
    return specs


SPATIAL_SOURCE_ROWS = [
    (
        1,
        "pick_up_the_black_bowl_between_the_plate_and_the_ramekin_and_place_it_on_the_plate",
        "between the plate and the ramekin",
        ["cookies", "wine", "butter", "chocolate_pudding"],
    ),
    (
        2,
        "pick_up_the_black_bowl_next_to_the_ramekin_and_place_it_on_the_plate",
        "next to the ramekin",
        ["cookies", "wine", "butter", "chocolate_pudding"],
    ),
    (
        3,
        "pick_up_the_black_bowl_from_table_center_and_place_it_on_the_plate",
        "at the table center",
        ["cookies", "ramekin", "wine", "butter", "chocolate_pudding"],
    ),
    (
        4,
        "pick_up_the_black_bowl_on_the_cookie_box_and_place_it_on_the_plate",
        "on the cookies box",
        ["ramekin"],
    ),
    (
        5,
        "pick_up_the_black_bowl_in_the_top_drawer_of_the_wooden_cabinet_and_place_it_on_the_plate",
        "in the top drawer of the wooden cabinet",
        ["cookies", "ramekin", "wine", "butter", "chocolate_pudding"],
    ),
    (
        6,
        "pick_up_the_black_bowl_on_the_ramekin_and_place_it_on_the_plate",
        "on the ramekin",
        ["chocolate_pudding"],
    ),
    (
        7,
        "pick_up_the_black_bowl_next_to_the_cookie_box_and_place_it_on_the_plate",
        "next to the cookies box",
        ["ramekin", "wine", "butter", "chocolate_pudding"],
    ),
    (
        8,
        "pick_up_the_black_bowl_on_the_stove_and_place_it_on_the_plate",
        "on the stove",
        ["cookies", "ramekin", "wine", "butter", "chocolate_pudding"],
    ),
    (
        9,
        "pick_up_the_black_bowl_next_to_the_plate_and_place_it_on_the_plate",
        "next to the plate",
        ["cookies", "ramekin", "wine", "butter", "chocolate_pudding"],
    ),
    (
        10,
        "pick_up_the_black_bowl_on_the_wooden_cabinet_and_place_it_on_the_plate",
        "on top of the wooden cabinet",
        ["cookies", "ramekin", "wine", "butter", "chocolate_pudding"],
    ),
]


LATTICE_OBJECTS = {
    "cookies": ("cookies box", "cookies_1", "cookies", None),
    "ramekin": (
        "ramekin",
        "glazed_rim_porcelain_ramekin_1",
        "glazed_rim_porcelain_ramekin",
        None,
    ),
    "wine": ("wine bottle", "wine_bottle_1", "wine_bottle", 5),
    "butter": ("butter", "butter_1", "butter", 307),
    "chocolate_pudding": (
        "chocolate pudding",
        "chocolate_pudding_1",
        "chocolate_pudding",
        309,
    ),
    "cream_cheese": ("cream cheese", "cream_cheese_1", "cream_cheese", 4),
    "plate": ("plate", "plate_1", "plate", 1),
    "black_bowl": ("black bowl", "akita_black_bowl_1", "akita_black_bowl", 1),
    "porcelain_mug": ("white mug", "porcelain_mug_1", "porcelain_mug", 104),
    "white_yellow_mug": (
        "yellow and white mug",
        "white_yellow_mug_1",
        "white_yellow_mug",
        104,
    ),
}


def lattice_object_evidence(key: str) -> str:
    if key in {"cookies", "ramekin"}:
        return (
            "Training evidence: this object appears in original Spatial scenes only as a distractor/support; "
            "no LIBERO-40 trajectory directly grasps it."
        )
    if key in {"butter", "chocolate_pudding"}:
        source_id = LATTICE_OBJECTS[key][3]
        return f"Training evidence: direct package grasp in original LIBERO-Object task {source_id}."
    if key == "wine":
        return "Training evidence: direct wine-bottle grasp in original LIBERO-Goal tasks."
    if key == "plate":
        return "Training evidence: the plate is directly manipulated by the original Goal push task, but not by pick-and-place."
    if key == "black_bowl":
        return "Training evidence: direct black-bowl grasp in original Spatial and Goal tasks."
    if key == "cream_cheese":
        return "Training evidence: direct cream-cheese grasp in original Goal and LIBERO-Object tasks."
    if key in {"porcelain_mug", "white_yellow_mug"}:
        return "Training evidence: direct mug grasp in original LIBERO-10 tasks."
    return "Training evidence: recorded in the source metadata."


def spatial_scene_lattice_specs(start: int) -> list[base.Spec]:
    """Enumerate the finite Spatial scene-position/object/target lattice."""
    specs: list[base.Spec] = []
    idx = start
    sources: dict[int, tuple[Path, Path, str, list[str]]] = {}
    for scene_index, stem, position_phrase, replacements in SPATIAL_SOURCE_ROWS:
        bddl, init_path = source("libero_spatial", stem)
        sources[scene_index] = (bddl, init_path, position_phrase, replacements)

    # Keep the original source position/object and transfer only the learned
    # destination.  Initial-on-target cases are excluded before simulation.
    destination_rows = [
        (
            "top of the wooden cabinet",
            "wooden_cabinet_1_top_side",
            "wooden_cabinet_1",
            "body_prefix",
        ),
        ("stove", "flat_stove_1_cook_region", "flat_stove_1", "body_prefix"),
    ]
    for scene_index in range(1, 11):
        bddl, init_path, position_phrase, _ = sources[scene_index]
        for destination_label, target, mask_value, mask_kind in destination_rows:
            if (scene_index == 10 and target == "wooden_cabinet_1_top_side") or (
                scene_index == 8 and target == "flat_stove_1_cook_region"
            ):
                continue
            language = (
                f"Pick up the black bowl {position_phrase} and place it on the "
                f"{destination_label}."
            )
            specs.append(
                mk_spec(
                    f"ANLGX_{idx:03d}",
                    "S1_spatial_source_to_learned_destination",
                    language,
                    bddl,
                    init_path,
                    "libero_spatial",
                    None,
                    f"on(akita_black_bowl_1, {target})",
                    f"(On akita_black_bowl_1 {target})",
                    ["akita_black_bowl_1", target],
                    base.pick_place("akita_black_bowl_1", target, None, language),
                    [
                        base.selector(
                            "manipulated_object", "body_prefix", "akita_black_bowl_1", "green"
                        ),
                        base.selector("goal_target", mask_kind, mask_value, "yellow"),
                    ],
                    base.identity,
                    [f"transfer the learned destination to the Spatial-{scene_index:02d} start relation"],
                    ["full Spatial source context", "black-bowl identity and source relation"],
                    ["akita_black_bowl_1"],
                    f"spatial_{scene_index:02d}_original_context",
                )
            )
            idx += 1

    def basket_transform(text: str) -> str:
        output = clean_scene(
            [
                region("basket_region", "main_table", (0.02, -0.28, 0.04, -0.26), 3.141592653589793),
                region("contain_region", "basket_1"),
            ],
            ["main_table - table"],
            ["basket_1 - basket"],
            ["(On basket_1 main_table_basket_region)"],
        )(text)
        return remove_fixture_instance(output, "wooden_cabinet_1")

    # The cabinet footprint is replaced by a learned basket target in the
    # three distinct Spatial-1/2/3 object layouts.
    for scene_index in (1, 2, 3):
        bddl, init_path, position_phrase, _ = sources[scene_index]
        language = f"Pick up the black bowl {position_phrase} and put it in the basket."
        specs.append(
            mk_spec(
                f"ANLGX_{idx:03d}",
                "S2_spatial_cabinet_to_basket_target_transfer",
                language,
                bddl,
                init_path,
                "libero_spatial",
                None,
                "in(akita_black_bowl_1, basket_1_contain_region)",
                "(In akita_black_bowl_1 basket_1_contain_region)",
                ["akita_black_bowl_1", "basket_1_contain_region"],
                base.pick_place("akita_black_bowl_1", "basket_1_contain_region", None, language),
                [
                    base.selector("manipulated_object", "body_prefix", "akita_black_bowl_1", "green"),
                    base.selector("goal_target", "body_prefix", "basket_1", "yellow"),
                ],
                basket_transform,
                ["replace the cabinet footprint with a reachable basket target"],
                ["Spatial source objects and source relation except the overlapping cabinet"],
                ["akita_black_bowl_1", "basket_1"],
                f"spatial_{scene_index:02d}_basket_replaces_cabinet",
                ["The wooden cabinet is removed only because the basket occupies its footprint."],
            )
        )
        idx += 1

    # Put the original plate into that basket.  The three rows intentionally
    # share language but retain distinct official Spatial scene contexts.
    for scene_index in (1, 2, 3):
        bddl, init_path, _, _ = sources[scene_index]
        language = "Put the plate in the basket."
        specs.append(
            mk_spec(
                f"ANLGX_{idx:03d}",
                "S2_spatial_cabinet_to_basket_target_transfer",
                language,
                bddl,
                init_path,
                "libero_spatial",
                None,
                "in(plate_1, basket_1_contain_region)",
                "(In plate_1 basket_1_contain_region)",
                ["plate_1", "basket_1_contain_region"],
                base.pick_place("plate_1", "basket_1_contain_region", None, language),
                [
                    base.selector("manipulated_object", "body_prefix", "plate_1", "green"),
                    base.selector("goal_target", "body_prefix", "basket_1", "yellow"),
                ],
                basket_transform,
                ["bind the learned basket relation to the plate in a Spatial source scene"],
                ["source plate pose", "source objects except the replaced cabinet"],
                ["plate_1", "basket_1"],
                f"spatial_{scene_index:02d}_basket_replaces_cabinet",
                [
                    "Same instruction, three distinct official Spatial object layouts.",
                    lattice_object_evidence("plate"),
                ],
            )
        )
        idx += 1

    def rack_transform(text: str) -> str:
        transformed = clean_scene(
            [
                # Mirror only the y coordinate of the official Goal rack
                # center (-0.26, -0.26). In the agent view this is the true
                # right-side counterpart, with the same robot-facing yaw.
                region("wine_rack_region", "main_table", (-0.27, 0.25, -0.25, 0.27), 3.141592653589793),
                region("top_region", "wine_rack_1"),
            ],
            ["main_table - table", "wine_rack_1 - wine_rack"],
            [],
            ["(On wine_rack_1 main_table_wine_rack_region)"],
        )(text)
        transformed = remove_object_instance(
            transformed, "glazed_rim_porcelain_ramekin_1"
        )
        transformed = remove_object_instance(transformed, "akita_black_bowl_2")
        return remove_fixture_instance(transformed, "flat_stove_1")

    scene10_bddl, scene10_init, scene10_position, _ = sources[10]
    for label, object_id, object_type, source_id in (
        LATTICE_OBJECTS["black_bowl"],
        LATTICE_OBJECTS["wine"],
    ):
        transform: Callable[[str], str]
        if object_id == "akita_black_bowl_1":
            transform = rack_transform
        else:
            def transform(
                text: str,
                *,
                new_id: str = object_id,
                new_type: str = object_type,
            ) -> str:
                return rack_transform(
                    replace_object_identity(text, "akita_black_bowl_1", new_id, new_type)
                )
        language = f"Pick up the {label} {scene10_position} and put it on the wine rack."
        specs.append(
            mk_spec(
                f"ANLGX_{idx:03d}",
                "S3_spatial_cabinet_start_to_added_rack",
                language,
                scene10_bddl,
                scene10_init,
                "libero_spatial",
                source_id,
                f"on({object_id}, wine_rack_1_top_region)",
                f"(On {object_id} wine_rack_1_top_region)",
                [object_id, "wine_rack_1_top_region"],
                base.pick_place(object_id, "wine_rack_1_top_region", source_id, language),
                [
                    base.selector("manipulated_object", "body_prefix", object_id, "green"),
                    base.selector("goal_target", "body_prefix", "wine_rack_1", "yellow"),
                ],
                transform,
                ["add a right-side rack at an official reachable fixture orientation"],
                ["Spatial-10 cabinet start relation and nonblocking source context"],
                ["wine_rack_1"],
                f"spatial_10_added_right_rack_{object_type}",
                [
                    "The rack uses the validated Goal right-side mirror pose; the source ramekin overlaps its footprint, and the stove plus second bowl block the cabinet-to-rack corridor, so only those blockers are removed.",
                    "Init gate: after settling, the manipulated object must still satisfy On(object, wooden-cabinet top); support-preserving roll is allowed.",
                    lattice_object_evidence(
                        "black_bowl" if object_id == "akita_black_bowl_1" else "wine"
                    ),
                ],
            )
        )
        idx += 1

    # Replace only the source manipuland while preserving its exact official
    # Spatial relation, then use the original learned plate destination.
    for scene_index, (bddl, init_path, position_phrase, replacement_keys) in sources.items():
        for key in replacement_keys:
            label, object_id, object_type, source_id = LATTICE_OBJECTS[key]

            def transform(
                text: str,
                *,
                new_id: str = object_id,
                new_type: str = object_type,
            ) -> str:
                return replace_object_identity(text, "akita_black_bowl_1", new_id, new_type)

            language = f"Pick up the {label} {position_phrase} and place it on the plate."
            semantic_support_scene = scene_index in {4, 5, 6, 8, 10}
            critical_objects = [object_id, "plate_1"]
            support_note: list[str] = []
            if semantic_support_scene:
                # A substituted object may roll or tip while remaining
                # semantically on/in its instructed support.  Validate that
                # predicate directly instead of rejecting harmless rotation.
                critical_objects = ["plate_1"]
                support_note.append(
                    "Init gate: after settling, the substituted object must still satisfy its exact source support predicate; support-preserving rotation is allowed."
                )
            specs.append(
                mk_spec(
                    f"ANLGX_{idx:03d}",
                    "S4_spatial_source_object_binding",
                    language,
                    bddl,
                    init_path,
                    "libero_spatial",
                    source_id,
                    f"on({object_id}, plate_1)",
                    f"(On {object_id} plate_1)",
                    [object_id, "plate_1"],
                    base.pick_place(object_id, "plate_1", source_id, language),
                    [
                        base.selector("manipulated_object", "body_prefix", object_id, "green"),
                        base.selector("goal_target", "body_prefix", "plate_1", "yellow"),
                    ],
                    transform,
                    [f"replace the source bowl with {label} at the same learned Spatial relation"],
                    ["full source layout", "plate target pose", "single On predicate"],
                    critical_objects,
                    f"spatial_{scene_index:02d}_source_object_{object_type}",
                    [
                        "Reference-identity collisions are excluded: the replaced object is never the ramekin/cookies/plate named by its own source relation.",
                        lattice_object_evidence(key),
                        *support_note,
                    ],
                )
            )
            idx += 1

    # Sibling drawer actions in one representative Spatial layout.  All ten
    # official Spatial tasks share the same cabinet pose; duplicate contexts
    # are collapsed unless they change the interaction corridor.
    scene1_bddl, scene1_init, _, _ = sources[1]
    for action_type in ("open", "close"):
        for slot in ("top", "middle", "bottom"):
            target = f"wooden_cabinet_1_{slot}_region"
            language = f"{action_type.title()} the {slot} drawer of the wooden cabinet."
            transform = base.identity
            if action_type == "close":
                transform = lambda text, slot=slot: base.replace_open_init(
                    text, "wooden_cabinet_1", slot
                )
            specs.append(
                mk_spec(
                    f"ANLGX_{idx:03d}",
                    "S5_spatial_sibling_drawer_action",
                    language,
                    scene1_bddl,
                    scene1_init,
                    "libero_spatial",
                    10 if action_type == "open" else 108,
                    f"{action_type}({target})",
                    f"({action_type.title()} {target})",
                    [target],
                    [base.action(action_type, target, target, 10 if action_type == "open" else 108, language)],
                    [base.selector("interaction_target", "drawer_part", f"wooden_cabinet_1:{slot}", "green")],
                    transform,
                    [f"apply the learned {action_type} primitive to the {slot} sibling drawer in a Spatial scene"],
                    ["Spatial-1 objects and cabinet pose"],
                    [],
                    f"spatial_01_wooden_drawer_{action_type}_{slot}",
                )
            )
            idx += 1

    assert idx == start + 71, (idx, start)
    return specs


def goal_scene_lattice_specs(start: int) -> list[base.Spec]:
    """Enumerate Goal-scene object, target, sibling, and donor-pose bindings."""
    specs: list[base.Spec] = []
    idx = start

    def replaced(old_id: str, key: str) -> tuple[str, str, str, int | None, Callable[[str], str]]:
        label, object_id, object_type, source_id = LATTICE_OBJECTS[key]

        def transform(text: str) -> str:
            return replace_object_identity(text, old_id, object_id, object_type)

        return label, object_id, object_type, source_id, transform

    relation_rows = [
        {
            "family": "G1_goal_object_to_stove",
            "source_bddl": GOAL_BOWL_STOVE,
            "source_init": GOAL_BOWL_STOVE_INIT,
            "old_id": "akita_black_bowl_1",
            "keys": ["wine", "butter", "chocolate_pudding", "cream_cheese", "plate"],
            "target": "flat_stove_1_cook_region",
            "target_label": "stove",
            "target_mask": "flat_stove_1",
            "source_relation_id": 8,
        },
        {
            "family": "G2_goal_object_to_rack",
            "source_bddl": GOAL_WINE_RACK,
            "source_init": GOAL_WINE_RACK_INIT,
            "old_id": "wine_bottle_1",
            "keys": ["black_bowl", "plate", "butter", "chocolate_pudding", "cream_cheese"],
            "target": "wine_rack_1_top_region",
            "target_label": "wine rack",
            "target_mask": "wine_rack_1",
            "source_relation_id": 2,
        },
        {
            "family": "G3_goal_object_to_cabinet_top",
            "source_bddl": GOAL_WINE_CABINET,
            "source_init": GOAL_WINE_CABINET_INIT,
            "old_id": "wine_bottle_1",
            "keys": ["plate", "cream_cheese", "butter", "chocolate_pudding"],
            "target": "wooden_cabinet_1_top_side",
            "target_label": "top of the wooden cabinet",
            "target_mask": "wooden_cabinet_1",
            "source_relation_id": 5,
        },
        {
            "family": "G4_goal_object_to_bowl",
            "source_bddl": GOAL_CREAM_BOWL,
            "source_init": GOAL_CREAM_BOWL_INIT,
            "old_id": "cream_cheese_1",
            "keys": ["butter", "chocolate_pudding"],
            "target": "akita_black_bowl_1",
            "target_label": "black bowl",
            "target_mask": "akita_black_bowl_1",
            "source_relation_id": 4,
        },
        {
            "family": "G5_goal_object_to_plate",
            "source_bddl": GOAL_BOWL_PLATE,
            "source_init": GOAL_BOWL_PLATE_INIT,
            "old_id": "akita_black_bowl_1",
            "keys": ["wine", "cream_cheese", "butter", "chocolate_pudding"],
            "target": "plate_1",
            "target_label": "plate",
            "target_mask": "plate_1",
            "source_relation_id": 1,
        },
    ]
    for row in relation_rows:
        for key in row["keys"]:
            label, object_id, object_type, source_id, transform = replaced(str(row["old_id"]), key)
            language = f"Put the {label} on the {row['target_label']}."
            target = str(row["target"])
            specs.append(
                mk_spec(
                    f"ANLGX_{idx:03d}",
                    str(row["family"]),
                    language,
                    Path(row["source_bddl"]),
                    Path(row["source_init"]),
                    "libero_goal",
                    source_id,
                    f"on({object_id}, {target})",
                    f"(On {object_id} {target})",
                    [object_id, target],
                    base.pick_place(object_id, target, source_id, language),
                    [
                        base.selector("manipulated_object", "body_prefix", object_id, "green"),
                        base.selector("goal_target", "body_prefix", str(row["target_mask"]), "yellow"),
                    ],
                    transform,
                    [f"bind {label} to the learned Goal relation and target"],
                    ["Goal scene fixture poses", "source-scene context", "single On predicate"],
                    [object_id],
                    f"goal_relation_{str(row['family']).lower()}_{object_type}",
                    [
                        f"Relation evidence: original Goal task {row['source_relation_id']}; the source manipuland pose is preserved.",
                        lattice_object_evidence(key),
                    ],
                )
            )
            idx += 1

    # Drawer insertion is atomic: the selected sibling drawer is already open
    # in init.  Original top-bowl decomposition and the two existing bowl
    # sibling tasks are not repeated here.
    for key in ("wine", "cream_cheese", "butter", "chocolate_pudding"):
        label, object_id, object_type, source_id, replace_transform = replaced(
            "akita_black_bowl_1", key
        )
        for slot in ("top", "middle", "bottom"):
            target = f"wooden_cabinet_1_{slot}_region"

            def transform(
                text: str,
                *,
                slot: str = slot,
                replace_transform: Callable[[str], str] = replace_transform,
            ) -> str:
                return base.replace_open_init(
                    replace_transform(text), "wooden_cabinet_1", slot
                )

            language = f"Put the {label} in the {slot} drawer of the wooden cabinet."
            specs.append(
                mk_spec(
                    f"ANLGX_{idx:03d}",
                    "G6_goal_object_to_sibling_drawer",
                    language,
                    GOAL_INSERT_TOP,
                    GOAL_INSERT_TOP_INIT,
                    "libero_goal",
                    source_id,
                    f"in({object_id}, {target})",
                    f"(In {object_id} {target})",
                    [object_id, target],
                    base.pick_place(object_id, target, source_id, language),
                    [
                        base.selector("manipulated_object", "body_prefix", object_id, "green"),
                        base.selector("goal_target", "drawer_part", f"wooden_cabinet_1:{slot}", "yellow"),
                    ],
                    transform,
                    [f"replace the bowl with {label}", f"transfer top-drawer insertion to {slot}"],
                    ["wooden cabinet pose", "drawer initialized open", "single In predicate"],
                    [object_id],
                    f"goal_drawer_insert_{slot}_{object_type}",
                    [lattice_object_evidence(key)],
                )
            )
            idx += 1

    # Push the bowl from the learned plate start to the exact stove-front
    # region.  This deliberately tests the user's requested plate->bowl
    # transfer while keeping simulator-projected placement masks.
    bowl_label, bowl_id, bowl_type, bowl_source_id, bowl_transform = replaced(
        "plate_1", "black_bowl"
    )
    language = "Push the black bowl to the front of the stove."
    specs.append(
        mk_spec(
            f"ANLGX_{idx:03d}",
            "G7_goal_push_object_binding",
            language,
            GOAL_PUSH_STOVE,
            GOAL_PUSH_STOVE_INIT,
            "libero_goal",
            6,
            "on(akita_black_bowl_1, main_table_stove_front_region)",
            "(On akita_black_bowl_1 main_table_stove_front_region)",
            ["akita_black_bowl_1", "main_table_stove_front_region"],
            [
                base.action("approach", "akita_black_bowl_1", "akita_black_bowl_1", 6, language),
                base.action("push", "akita_black_bowl_1", "main_table_stove_front_region", 6, language),
            ],
            [
                base.selector("manipulated_object", "body_prefix", "akita_black_bowl_1", "green"),
                base.selector("goal_target", "table_region", "main_table_stove_front_region", "yellow"),
            ],
            bowl_transform,
            ["replace the source plate with a black bowl at the exact push start"],
            ["stove pose", "reference-relative front region", "single On predicate"],
            ["akita_black_bowl_1"],
            "goal_push_black_bowl_original_stove",
        )
    )
    idx += 1

    forward_stove_pose = (-0.21, 0.19, -0.19, 0.21)

    def move_goal_stove_forward(text: str) -> str:
        return base.replace_region_range(text, "stove_region", forward_stove_pose)

    # The black-bowl and Turnon versions at this donor pose already belong to
    # the reused E3 pool; enumerate the remaining compatible objects.
    for key in ("wine", "butter", "chocolate_pudding", "cream_cheese", "plate"):
        label, object_id, object_type, source_id, replace_transform = replaced(
            "akita_black_bowl_1", key
        )

        def transform(
            text: str,
            *,
            replace_transform: Callable[[str], str] = replace_transform,
        ) -> str:
            return move_goal_stove_forward(replace_transform(text))

        language = f"Put the {label} on the forward-relocated stove."
        specs.append(
            mk_spec(
                f"ANLGX_{idx:03d}",
                "G8_goal_object_to_forward_stove",
                language,
                GOAL_BOWL_STOVE,
                GOAL_BOWL_STOVE_INIT,
                "libero_goal",
                source_id,
                f"on({object_id}, flat_stove_1_cook_region)",
                f"(On {object_id} flat_stove_1_cook_region)",
                [object_id, "flat_stove_1_cook_region"],
                base.pick_place(object_id, "flat_stove_1_cook_region", source_id, language),
                [
                    base.selector("manipulated_object", "body_prefix", object_id, "green"),
                    base.selector("goal_target", "body_prefix", "flat_stove_1", "yellow"),
                ],
                transform,
                ["move the stove forward to the official Scene-3 donor x-position", f"replace the bowl with {label}"],
                ["stove yaw", "Goal scene context", "single On predicate"],
                [object_id],
                f"goal_forward_stove_{object_type}",
                [lattice_object_evidence(key)],
            )
        )
        idx += 1

    # Forward-stove bowl push; the original plate forward push is already E3.
    forward_front = (0.12, 0.16, 0.20, 0.24)

    def forward_bowl_push(text: str) -> str:
        output = bowl_transform(text)
        output = base.replace_region_range(output, "stove_region", forward_stove_pose)
        return base.replace_region_range(output, "stove_front_region", forward_front)

    language = "Push the black bowl to the front of the forward-relocated stove."
    specs.append(
        mk_spec(
            f"ANLGX_{idx:03d}",
            "G8_goal_object_to_forward_stove",
            language,
            GOAL_PUSH_STOVE,
            GOAL_PUSH_STOVE_INIT,
            "libero_goal",
            6,
            "on(akita_black_bowl_1, main_table_stove_front_region)",
            "(On akita_black_bowl_1 main_table_stove_front_region)",
            ["akita_black_bowl_1", "main_table_stove_front_region"],
            [
                base.action("approach", "akita_black_bowl_1", "akita_black_bowl_1", 6, language),
                base.action("push", "akita_black_bowl_1", "main_table_stove_front_region", 6, language),
            ],
            [
                base.selector("manipulated_object", "body_prefix", "akita_black_bowl_1", "green"),
                base.selector("goal_target", "table_region", "main_table_stove_front_region", "yellow"),
            ],
            forward_bowl_push,
            ["replace plate with bowl", "translate stove and its front region together"],
            ["Goal context", "stove yaw", "single On predicate"],
            ["akita_black_bowl_1"],
            "goal_forward_stove_push_black_bowl",
            ["The yellow mask is projected from the transformed current BDDL front region."],
        )
    )
    idx += 1

    mirrored_rack_pose = (-0.27, 0.25, -0.25, 0.27)
    for key in ("wine", "black_bowl", "plate", "butter", "chocolate_pudding", "cream_cheese"):
        if key == "wine":
            label, object_id, object_type, source_id = LATTICE_OBJECTS[key]
            replace_transform = base.identity
        else:
            label, object_id, object_type, source_id, replace_transform = replaced(
                "wine_bottle_1", key
            )

        def transform(
            text: str,
            *,
            replace_transform: Callable[[str], str] = replace_transform,
        ) -> str:
            output = replace_transform(text)
            output = base.replace_region_range(output, "wine_rack_region", mirrored_rack_pose)
            output = base.replace_region_yaw(output, "wine_rack_region", 3.141592653589793)
            return remove_fixture_instance(output, "flat_stove_1")

        language = f"Put the {label} on the right-side wine rack."
        specs.append(
            mk_spec(
                f"ANLGX_{idx:03d}",
                "G9_goal_object_to_mirrored_rack",
                language,
                GOAL_WINE_RACK,
                GOAL_WINE_RACK_INIT,
                "libero_goal",
                source_id,
                f"on({object_id}, wine_rack_1_top_region)",
                f"(On {object_id} wine_rack_1_top_region)",
                [object_id, "wine_rack_1_top_region"],
                base.pick_place(object_id, "wine_rack_1_top_region", source_id, language),
                [
                    base.selector("manipulated_object", "body_prefix", object_id, "green"),
                    base.selector("goal_target", "body_prefix", "wine_rack_1", "yellow"),
                ],
                transform,
                ["mirror the rack to the right side while keeping it robot-facing", f"bind {label} to the rack relation"],
                ["cabinet and nonblocking Goal context", "single On predicate"],
                [object_id, "wine_rack_1"],
                f"goal_right_rack_{object_type}",
                [
                    "The stove is removed because its original footprint overlaps the right-side rack.",
                    lattice_object_evidence(key),
                ],
            )
        )
        idx += 1

    # Close is learned in LIBERO-10; apply it atomically to all wooden drawer
    # siblings in the Goal scene, with the instructed drawer open at init.
    for slot in ("top", "middle", "bottom"):
        target = f"wooden_cabinet_1_{slot}_region"
        language = f"Close the {slot} drawer of the wooden cabinet."
        specs.append(
            mk_spec(
                f"ANLGX_{idx:03d}",
                "G10_goal_sibling_drawer_close",
                language,
                GOAL_OPEN_MIDDLE,
                GOAL_OPEN_MIDDLE_INIT,
                "libero_goal",
                108,
                f"close({target})",
                f"(Close {target})",
                [target],
                [base.action("close", target, target, 108, language)],
                [base.selector("interaction_target", "drawer_part", f"wooden_cabinet_1:{slot}", "green")],
                lambda text, slot=slot: base.replace_open_init(text, "wooden_cabinet_1", slot),
                [f"transfer learned drawer-close primitive to the Goal {slot} sibling"],
                ["Goal scene context", "wooden cabinet pose"],
                [],
                f"goal_wooden_drawer_close_{slot}",
            )
        )
        idx += 1

    assert idx == start + 48, (idx, start)
    return specs


def libero10_scene_lattice_specs(start: int) -> list[base.Spec]:
    """Add novel single-atom transfers in the official LIBERO-10 contexts."""
    specs: list[base.Spec] = []
    idx = start

    # White-cabinet scene: transfer the learned bowl insertion to the wine
    # bottle in every sibling drawer.  The selected drawer is open at init.
    for slot in ("top", "middle", "bottom"):
        target = f"white_cabinet_1_{slot}_region"

        def transform(text: str, *, slot: str = slot) -> str:
            output = replace_object_identity(
                text, "akita_black_bowl_1", "wine_bottle_1", "wine_bottle"
            )
            return base.replace_open_init(output, "white_cabinet_1", slot)

        language = f"Put the wine bottle in the {slot} drawer of the white cabinet."
        specs.append(
            mk_spec(
                f"ANLGX_{idx:03d}",
                "L1_libero10_white_cabinet_object_slot",
                language,
                KITCHEN4,
                KITCHEN4_INIT,
                "libero_10",
                108,
                f"in(wine_bottle_1, {target})",
                f"(In wine_bottle_1 {target})",
                ["wine_bottle_1", target],
                base.pick_place("wine_bottle_1", target, 108, language),
                [
                    base.selector("manipulated_object", "body_prefix", "wine_bottle_1", "green"),
                    base.selector("goal_target", "drawer_part", f"white_cabinet_1:{slot}", "yellow"),
                ],
                transform,
                ["replace the bowl with the scene's wine bottle", f"select the {slot} sibling drawer"],
                ["KITCHEN_SCENE4 context", "drawer initialized open", "single In predicate"],
                ["wine_bottle_1"],
                f"libero10_scene4_wine_insert_{slot}",
                [lattice_object_evidence("wine")],
            )
        )
        idx += 1

    # Atomic bottom close complements the existing top/middle sibling tasks;
    # the source long-task insertion atom is deliberately not required.
    language = "Close the bottom drawer of the white cabinet."
    specs.append(
        mk_spec(
            f"ANLGX_{idx:03d}",
            "L2_libero10_white_cabinet_atomic_close",
            language,
            KITCHEN4,
            KITCHEN4_INIT,
            "libero_10",
            108,
            "close(white_cabinet_1_bottom_region)",
            "(Close white_cabinet_1_bottom_region)",
            ["white_cabinet_1_bottom_region"],
            [base.action("close", "white_cabinet_1_bottom_region", "white_cabinet_1_bottom_region", 108, language)],
            [base.selector("interaction_target", "drawer_part", "white_cabinet_1:bottom", "green")],
            base.identity,
            ["retain only the close atom from the long task"],
            ["Scene-4 objects", "bottom drawer open at init"],
            [],
            "libero10_scene4_atomic_close_bottom",
        )
    )
    idx += 1

    # Caddy: replace the book with the scene's mug at the exact book start and
    # enumerate all four local sibling compartments.
    for compartment in ("back", "front", "left", "right"):
        target = f"desk_caddy_1_{compartment}_contain_region"
        language = f"Put the yellow and white mug in the {compartment} compartment of the caddy."
        specs.append(
            mk_spec(
                f"ANLGX_{idx:03d}",
                "L3_libero10_caddy_object_compartment",
                language,
                STUDY1,
                STUDY1_INIT,
                "libero_10",
                104,
                f"in(white_yellow_mug_1, {target})",
                f"(In white_yellow_mug_1 {target})",
                ["white_yellow_mug_1", target],
                base.pick_place("white_yellow_mug_1", target, 104, language),
                [
                    base.selector("manipulated_object", "body_prefix", "white_yellow_mug_1", "green"),
                    base.selector("goal_target", "body_prefix", "desk_caddy_1", "yellow"),
                ],
                lambda text: replace_object_identity(
                    text, "black_book_1", "white_yellow_mug_1", "white_yellow_mug"
                ),
                ["replace the book with a learned mug grasp", f"select the {compartment} sibling compartment"],
                ["caddy pose", "source scene context", "single In predicate"],
                ["white_yellow_mug_1"],
                "libero10_study1_mug_caddy_context",
                [lattice_object_evidence("white_yellow_mug")],
            )
        )
        idx += 1

    # Frypan-to-stove binding at the original long-task pose and two official
    # stove donor poses.  The full KITCHEN_SCENE3 context is retained.
    frypan_pose_rows = [
        ("original Scene-3", None),
        ("Goal donor", (-0.42, 0.20, -0.40, 0.22)),
        ("Spatial donor", (-0.42, -0.15, -0.40, -0.13)),
    ]
    for donor_label, pose in frypan_pose_rows:
        if pose is None:
            transform = base.identity
        else:
            transform = lambda text, pose=pose: base.replace_region_range(
                text, "flat_stove_init_region", pose
            )
        language = f"Put the frypan on the stove at the {donor_label} position."
        specs.append(
            mk_spec(
                f"ANLGX_{idx:03d}",
                "L4_libero10_frypan_stove_binding",
                language,
                KITCHEN3,
                KITCHEN3_INIT,
                "libero_10",
                101,
                "on(chefmate_8_frypan_1, flat_stove_1_cook_region)",
                "(On chefmate_8_frypan_1 flat_stove_1_cook_region)",
                ["chefmate_8_frypan_1", "flat_stove_1_cook_region"],
                base.pick_place("chefmate_8_frypan_1", "flat_stove_1_cook_region", 101, language),
                [
                    base.selector("manipulated_object", "body_prefix", "chefmate_8_frypan_1", "green"),
                    base.selector("goal_target", "body_prefix", "flat_stove_1", "yellow"),
                ],
                transform,
                ["bind the scene frypan to the learned stove-support relation", f"use {donor_label} stove pose"],
                ["moka pot and nonblocking Scene-3 context", "single On predicate"],
                ["chefmate_8_frypan_1"],
                f"libero10_scene3_frypan_{donor_label.lower().replace(' ', '_').replace('-', '_')}",
                [
                    "Training evidence: the frypan appears in original KITCHEN_SCENE3 as a distractor; no LIBERO-40 trajectory directly grasps it."
                ],
            )
        )
        idx += 1

    # Microwave: use the white mug learned elsewhere, at the original and two
    # reachable official fixture donor positions.  Replacing the source mug
    # also removes the duplicate white-mug distractor.
    microwave_pose_rows = [
        ("original Scene-6", None),
        ("Scene-3 donor", (-0.21, 0.19, -0.19, 0.21)),
        ("Scene-8 donor", (-0.21, -0.21, -0.19, -0.19)),
    ]
    for donor_label, pose in microwave_pose_rows:
        def transform(text: str, *, pose=pose) -> str:
            output = replace_object_identity(
                text, "white_yellow_mug_1", "porcelain_mug_1", "porcelain_mug"
            )
            if pose is not None:
                output = base.replace_region_range(output, "microwave_init_region", pose)
            return output

        language = f"Put the white mug in the microwave at the {donor_label} position."
        specs.append(
            mk_spec(
                f"ANLGX_{idx:03d}",
                "L5_libero10_microwave_object_pose",
                language,
                KITCHEN6,
                KITCHEN6_INIT,
                "libero_10",
                109,
                "in(porcelain_mug_1, microwave_1_heating_region)",
                "(In porcelain_mug_1 microwave_1_heating_region)",
                ["porcelain_mug_1", "microwave_1_heating_region"],
                base.pick_place("porcelain_mug_1", "microwave_1_heating_region", 109, language),
                [
                    base.selector("manipulated_object", "body_prefix", "porcelain_mug_1", "green"),
                    base.selector("goal_target", "body_prefix", "microwave_1", "yellow"),
                ],
                transform,
                ["replace the yellow-and-white mug with the white mug", f"use {donor_label} microwave pose"],
                ["single In predicate", "microwave open at init", "nonblocking Scene-6 context"],
                ["porcelain_mug_1"],
                f"libero10_scene6_white_mug_{donor_label.lower().replace(' ', '_').replace('-', '_')}",
                [lattice_object_evidence("porcelain_mug")],
            )
        )
        idx += 1

    assert idx == start + 14, (idx, start)
    return specs


def build_specs() -> list[base.Spec]:
    specs = (
        exact_plate_specs(1)
        + sibling_specs(13)
        + fixture_pose_specs(26)
        + receptacle_support_specs(41)
        + spatial_scene_lattice_specs(53)
        + goal_scene_lattice_specs(124)
        + libero10_scene_lattice_specs(172)
    )
    expected = [f"ANLGX_{index:03d}" for index in range(1, 186)]
    if [spec.task_id for spec in specs] != expected:
        raise RuntimeError("expanded candidate numbering is not sequential")
    if any(spec.source_suite == "libero_object" for spec in specs):
        raise RuntimeError("relation/layout donor scenes must not come from LIBERO-Object")
    return specs


def rules_document() -> str:
    return """# Context-preserving LIBERO Analogy rules

## Scope

- Relation and layout donor scenes come from the 30 original tasks in `libero_spatial`, `libero_goal`, and `libero_10`.
- The 10 original `libero_object` layouts are not enumerated as a new scene axis. Their trained package grasps may supply object evidence for butter/pudding substitutions.
- Every new task has one semantic goal atom. Compound source tasks may supply a learned primitive, but no new task is an `and` composition.
- Spatial, Goal, and LIBERO-10 are traversed as finite scene lattices: source relation, compatible manipuland, learned target, sibling part, and official fixture donor pose.

## Scene-context and blocker rule

- The source scene is preserved by default, including non-interacting objects and fixtures.
- An object or fixture is removed only when it overlaps a relocated target/fixture or physically blocks the source-to-goal manipulation corridor.
- Example: for white mug to right plate, the intervening yellow-and-white mug is removed because it caused the observed ANLG_012 collision; the nonblocking red mug remains.
- When a package object already exists as a distractor in a relation source scene, the duplicate is removed and the single instructed instance is placed at the source manipuland pose.
- Repeated targets are intentionally retained because choosing the instructed instance is the tested analogy.

## Finite candidate lattice

The count is finite and auditable; it is not produced by sampling arbitrary continuous coordinates.

| Family | Count | Enumerated variable |
|---|---:|---|
| E1 exact-instance selection | 12 | 2 mugs x 3 plates, 1 bowl x 3 plates, 1 cream cheese x 3 bowls |
| E2 sibling part/compartment | 13 | caddy compartments, cabinet insertion/open/close slots, drawer extraction slots |
| E3 reference-fixture pose transfer | 15 | stable stove/cabinet poses copied from original LIBERO-40 layouts, with relative regions translated |
| E4 receptacle/support transfer | 12 | caddy, microwave insert/atomic-close, basket, rack, and cabinet-top transfers |
| S1-S5 Spatial scene lattice | 71 | ten official source relations, compatible objects, learned destinations, basket/rack grafts, drawer siblings |
| G1-G10 Goal scene lattice | 48 | object-target rebinding, drawer slots, push-object transfer, forward stove, mirrored rack |
| L1-L5 LIBERO-10 single-atom lattice | 14 | white-cabinet slots/close, caddy compartments, frypan-stove, microwave object/pose |
| **Total** | **185** | 52 reusable structural/pose candidates + 133 new scene-lattice candidates |

## Position evidence

- Stove donors are the exact Goal, Spatial, LIBERO-10 Scene 3, and Scene 8 fixture coordinates.
- Cabinet donor is the exact LIBERO-10 white-cabinet coordinate with an arm-facing yaw.
- Caddy donors are original book/mug interaction slots.
- Basket donor is an original grasped-object slot.
- Reference-identity collisions are excluded before simulation (for example, the object described as being next to the ramekin is never itself the only ramekin).
- Same-instruction rows are retained only when they represent distinct official source layouts; this is recorded in each task's physical group and source provenance.
- No claim is made that 185 is the mathematical maximum over continuous SE(2); it is the complete stable count for the explicit finite rules above.

## Masks

- Masks are resolved against the current simulator by exact instance.
- `plate_1`, `plate_2`, and `plate_3`, and all repeated bowls, are never unioned.
- Drawer masks select the instructed top/middle/bottom drawer body.
- Stove-front masks are projected from each current BDDL after relocation.
- JSON/source-episode fallback masks are forbidden during evaluation.
"""


def validate(root: Path, specs: list[base.Spec], bundles: dict[str, Path], state_count: int) -> None:
    signatures: set[str] = set()
    hashes: set[str] = set()
    for spec in specs:
        bundle = bundles[spec.task_id]
        meta = base.load_yaml(bundle / "task_meta.yaml")
        signature = str(meta["canonical_task_signature"])
        if signature in signatures:
            raise RuntimeError(f"duplicate signature: {signature}")
        signatures.add(signature)
        digest = hashlib.sha256(base.normalized_bddl(bundle / "task.bddl").encode()).hexdigest()
        if digest in hashes:
            raise RuntimeError(f"duplicate normalized BDDL: {spec.task_id}")
        hashes.add(digest)
        if len(base.load_init_array(bundle / "task.pruned_init")) != state_count:
            raise RuntimeError(f"wrong init-state count: {spec.task_id}")
        text = (bundle / "task.bddl").read_text(encoding="utf-8")
        # Only the demonstrated path blockers are removed; other source-scene
        # context must remain.  These two cases encode the user-reviewed mug
        # collisions in the three-plate scene.
        if spec.task_id == "ANLGX_003" and "white_yellow_mug_1" in text:
            raise RuntimeError("ANLGX_003: the right-plate corridor blocker remains")
        if spec.task_id == "ANLGX_004" and "porcelain_mug_1" in text:
            raise RuntimeError("ANLGX_004: the left-plate corridor blocker remains")
        if spec.task_id == "ANLGX_003" and "red_coffee_mug_1" not in text:
            raise RuntimeError("ANLGX_003: nonblocking source context was removed")
        if spec.task_id == "ANLGX_004" and "red_coffee_mug_1" not in text:
            raise RuntimeError("ANLGX_004: nonblocking source context was removed")

    family_counts: dict[str, int] = {}
    for spec in specs:
        family_counts[spec.family] = family_counts.get(spec.family, 0) + 1
    expected_family_counts = {
        "E1_clean_exact_instance_three_targets": 12,
        "E2_sibling_part_or_compartment": 13,
        "E3_reference_fixture_pose_transfer": 15,
        "E4_clean_receptacle_or_support_transfer": 12,
        "S1_spatial_source_to_learned_destination": 18,
        "S2_spatial_cabinet_to_basket_target_transfer": 6,
        "S3_spatial_cabinet_start_to_added_rack": 2,
        "S4_spatial_source_object_binding": 39,
        "S5_spatial_sibling_drawer_action": 6,
        "G1_goal_object_to_stove": 5,
        "G2_goal_object_to_rack": 5,
        "G3_goal_object_to_cabinet_top": 4,
        "G4_goal_object_to_bowl": 2,
        "G5_goal_object_to_plate": 4,
        "G6_goal_object_to_sibling_drawer": 12,
        "G7_goal_push_object_binding": 1,
        "G8_goal_object_to_forward_stove": 6,
        "G9_goal_object_to_mirrored_rack": 6,
        "G10_goal_sibling_drawer_close": 3,
        "L1_libero10_white_cabinet_object_slot": 3,
        "L2_libero10_white_cabinet_atomic_close": 1,
        "L3_libero10_caddy_object_compartment": 4,
        "L4_libero10_frypan_stove_binding": 3,
        "L5_libero10_microwave_object_pose": 3,
    }
    if family_counts != expected_family_counts:
        raise RuntimeError(f"unexpected family counts: {family_counts}")
    base.dump_yaml(
        root / "VALIDATION.yaml",
        {
            "task_count": len(specs),
            "sequential_ids": True,
            "id_range": ["ANLGX_001", "ANLGX_185"],
            "source_suites": ["libero_spatial", "libero_goal", "libero_10"],
            "relation_layout_donor_from_libero_object": False,
            "libero_object_used_as_object_grasp_evidence": True,
            "family_counts": family_counts,
            "unique_canonical_signatures": len(signatures),
            "unique_normalized_bddls": len(hashes),
            "init_states_per_task": state_count,
            "source_context_preserved_by_default": True,
            "overlap_and_path_blocker_gate": True,
            "rejected_candidate_count": 3,
            "rejected_candidate_index": "REJECTED_CANDIDATES.tsv",
            "simulator_render_and_mask_validation": True,
            "policy_inference_run": False,
        },
    )


def physical_init_signature(text: str) -> str:
    """Hash only model-defining scene sections, excluding language and goal."""
    parts: list[str] = []
    for start, end in (
        ("regions", "fixtures"),
        ("fixtures", "objects"),
        ("objects", "obj_of_interest"),
        ("init", "goal"),
    ):
        body = section_body(text, start, end).lower()
        parts.append(re.sub(r"\s+", "", body))
    return hashlib.sha256("\n".join(parts).encode("utf-8")).hexdigest()


def required_init_predicates(spec: base.Spec) -> list[tuple[str, str, str]]:
    if spec.family == "E2_sibling_part_or_compartment" and spec.physical_group.startswith(
        "wooden_extract_"
    ):
        slot = spec.physical_group.removeprefix("wooden_extract_")
        return [("in", "akita_black_bowl_1", f"wooden_cabinet_1_{slot}_region")]
    if spec.family == "S3_spatial_cabinet_start_to_added_rack":
        return [("on", spec.objects_of_interest[0], "wooden_cabinet_1_top_side")]
    if spec.family == "S4_spatial_source_object_binding":
        match = re.match(r"spatial_(\d{2})_source_object_", spec.physical_group)
        if match:
            source_supports = {
                4: ("on", "cookies_1"),
                5: ("in", "wooden_cabinet_1_top_region"),
                6: ("on", "glazed_rim_porcelain_ramekin_1"),
                8: ("on", "flat_stove_1_cook_region"),
                10: ("on", "wooden_cabinet_1_top_side"),
            }
            source_scene = int(match.group(1))
            if source_scene in source_supports:
                predicate, target = source_supports[source_scene]
                return [(predicate, spec.objects_of_interest[0], target)]
    return []


def copy_or_generate_init_parallel(
    specs: list[base.Spec],
    bundles: dict[str, Path],
    bddl_by_id: dict[str, str],
    state_count: int,
) -> None:
    """Generate unique physical groups on one lane each on GPUs 6 and 7."""
    cache_root = HERE / ".LiberoAnalogy_state_cache"
    cache_root.mkdir(exist_ok=True)
    representatives: dict[str, Path] = {}
    jobs: list[tuple[int, base.Spec, Path, Path]] = []
    total = len(specs)

    for index, spec in enumerate(specs, start=1):
        destination = bundles[spec.task_id] / "task.pruned_init"
        if spec.copied_from is not None:
            copied = base.load_init_array(spec.copied_from / "task.pruned_init")
            if len(copied) < state_count:
                raise RuntimeError(
                    f"{spec.task_id}: copied source has {len(copied)} states, expected {state_count}"
                )
            base.save_init_array(destination, copied[:state_count])
            representatives[spec.physical_group] = destination
            print(f"[{index:03d}/{total}] {spec.task_id}: copied validated states", flush=True)
            continue
        if spec.physical_group in representatives:
            continue
        source_text = spec.source_bddl.read_text(encoding="utf-8")
        if physical_init_signature(bddl_by_id[spec.task_id]) == physical_init_signature(
            source_text
        ):
            source_states = base.load_init_array(spec.source_init)
            if len(source_states) < state_count:
                raise RuntimeError(
                    f"{spec.task_id}: source archive has {len(source_states)} states, expected {state_count}"
                )
            base.save_init_array(destination, source_states[:state_count])
            representatives[spec.physical_group] = destination
            print(
                f"[{index:03d}/{total}] {spec.task_id}: reused {state_count} source-validated physical states",
                flush=True,
            )
            continue
        cache_payload = (
            bddl_by_id[spec.task_id]
            + f"\nstate_count={state_count}"
            + f"\ncritical={','.join(spec.critical_objects)}"
        )
        init_predicates = required_init_predicates(spec)
        if init_predicates:
            cache_payload += f"\nrequired_init={init_predicates}"
        cache_key = hashlib.sha256(cache_payload.encode("utf-8")).hexdigest()[:20]
        cache_path = cache_root / f"{spec.physical_group}__{cache_key}.pruned_init"
        if cache_path.is_file() and len(base.load_init_array(cache_path)) == state_count:
            shutil.copy2(cache_path, destination)
            representatives[spec.physical_group] = destination
            print(
                f"[{index:03d}/{total}] {spec.task_id}: restored {state_count} states from hash cache",
                flush=True,
            )
            continue
        representatives[spec.physical_group] = destination
        jobs.append((index, spec, destination, cache_path))

    worker = HERE / "run_analogy_init_worker.py"
    stop_event = threading.Event()

    def lane(gpu: int, lane_jobs: list[tuple[int, base.Spec, Path, Path]]) -> None:
        for index, spec, destination, cache_path in lane_jobs:
            if stop_event.is_set():
                return
            command = [
                sys.executable,
                str(worker),
                "--bddl",
                str(bundles[spec.task_id] / "task.bddl"),
                "--source-init",
                str(spec.source_init),
                "--output",
                str(destination),
                "--state-count",
                str(state_count),
                "--seed-base",
                str(310_000 + index * 1_000),
                "--gpu",
                str(gpu),
                "--critical",
                *spec.critical_objects,
            ]
            for predicate in required_init_predicates(spec):
                command.extend(["--required-predicate", *predicate])
            completed = subprocess.run(
                command,
                cwd=HERE,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                check=False,
            )
            if completed.stdout:
                print(completed.stdout.rstrip(), flush=True)
            if completed.returncode != 0:
                stop_event.set()
                raise RuntimeError(
                    f"{spec.task_id}: init worker on GPU {gpu} exited {completed.returncode}"
                )
            if len(base.load_init_array(destination)) != state_count:
                raise RuntimeError(f"{spec.task_id}: worker wrote the wrong state count")
            shutil.copy2(destination, cache_path)
            print(
                f"[{index:03d}/{total}] {spec.task_id}: generated {state_count} stable states on GPU {gpu}",
                flush=True,
            )

    lanes = {6: jobs[0::2], 7: jobs[1::2]}
    if jobs:
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            futures = [executor.submit(lane, gpu, lanes[gpu]) for gpu in (6, 7)]
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception:
                    stop_event.set()
                    raise

    # All tasks with the same physical initial scene reuse their representative
    # archive after both lanes have completed.
    for index, spec in enumerate(specs, start=1):
        destination = bundles[spec.task_id] / "task.pruned_init"
        representative = representatives[spec.physical_group]
        if destination != representative:
            shutil.copy2(representative, destination)
            print(
                f"[{index:03d}/{total}] {spec.task_id}: reused physical group {spec.physical_group}",
                flush=True,
            )


def render_comparisons_parallel(
    specs: list[base.Spec], root: Path
) -> dict[str, dict[str, int]]:
    """Render alternating task lanes concurrently on physical GPUs 6 and 7."""
    worker = HERE / "run_analogy_render_worker.py"
    result_paths = {
        6: root / ".render_gpu6.json",
        7: root / ".render_gpu7.json",
    }
    lanes = {6: specs[0::2], 7: specs[1::2]}

    def lane(gpu: int) -> None:
        command = [
            sys.executable,
            str(worker),
            "--root",
            str(root),
            "--gpu",
            str(gpu),
            "--result-json",
            str(result_paths[gpu]),
        ]
        for spec in lanes[gpu]:
            command.extend(["--task-id", spec.task_id])
        subprocess.run(command, cwd=HERE, check=True)

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        futures = [executor.submit(lane, gpu) for gpu in (6, 7)]
        for future in futures:
            future.result()

    results: dict[str, dict[str, int]] = {}
    for gpu in (6, 7):
        payload = yaml.safe_load(result_paths[gpu].read_text(encoding="utf-8")) or {}
        results.update(
            {
                str(task_id): {str(role): int(area) for role, area in areas.items()}
                for task_id, areas in payload.items()
            }
        )
        result_paths[gpu].unlink()
    if set(results) != {spec.task_id for spec in specs}:
        raise RuntimeError("parallel render results are incomplete")

    pair_paths = [
        next((root / "comparison_png").glob(f"{spec.task_id}__*.png"))
        for spec in specs
    ]
    thumb_w, thumb_h, columns = 320, 238, 4
    rows = (len(pair_paths) + columns - 1) // columns
    sheet = Image.new("RGB", (columns * thumb_w, rows * thumb_h), "#e9e5dc")
    for index, path in enumerate(pair_paths):
        image = Image.open(path).convert("RGB")
        image.thumbnail((thumb_w - 8, thumb_h - 8), Image.Resampling.LANCZOS)
        x_value = (index % columns) * thumb_w + (thumb_w - image.width) // 2
        y_value = (index // columns) * thumb_h + (thumb_h - image.height) // 2
        sheet.paste(image, (x_value, y_value))
    sheet.save(root / "comparison_png/ALL_ANALOGY_CANDIDATES_CONTACT_SHEET.png")
    return results


def reuse_validated_comparisons(
    specs: list[base.Spec],
    bundles: dict[str, Path],
    source_root: Path,
    stage: Path,
    rerender_changed: bool = False,
) -> dict[str, dict[str, int]]:
    """Reuse PNGs only when every current BDDL and exact mask still matches."""
    source_png = source_root / "comparison_png"
    if not source_png.is_dir():
        raise FileNotFoundError(source_png)
    results: dict[str, dict[str, int]] = {}
    changed_specs: list[base.Spec] = []
    raw_root = source_png / "raw"
    for spec in specs:
        source_bundles = list((source_root / "tasks").glob(f"{spec.task_id.lower()}__*"))
        if len(source_bundles) != 1:
            raise RuntimeError(
                f"{spec.task_id}: expected one comparison-source bundle, found {source_bundles}"
            )
        if base.normalized_bddl(source_bundles[0] / "task.bddl") != base.normalized_bddl(
            bundles[spec.task_id] / "task.bddl"
        ):
            if rerender_changed:
                changed_specs.append(spec)
                continue
            raise RuntimeError(f"{spec.task_id}: BDDL changed; comparison reuse is unsafe")
        pair_paths = list(source_png.glob(f"{spec.task_id}__*.png"))
        if len(pair_paths) != 1:
            raise RuntimeError(f"{spec.task_id}: expected one comparison PNG")
        areas: dict[str, int] = {}
        for binding in spec.masks:
            mask_path = raw_root / f"{spec.task_id}__mask_{binding.role}.png"
            if not mask_path.is_file():
                raise FileNotFoundError(mask_path)
            area = int((np.asarray(Image.open(mask_path)) > 0).sum())
            if area <= 0:
                raise RuntimeError(f"{spec.task_id}: empty reused mask {binding.role}")
            areas[binding.role] = area
        results[spec.task_id] = areas
    shutil.copytree(source_png, stage / "comparison_png")
    if changed_specs:
        for spec in changed_specs:
            for stale in (stage / "comparison_png").glob(f"{spec.task_id}__*.png"):
                stale.unlink()
            for stale in (stage / "comparison_png/raw").glob(f"{spec.task_id}__*.png"):
                stale.unlink()
        result_json = stage / ".rerender_changed.json"
        command = [
            sys.executable,
            str(HERE / "run_analogy_render_worker.py"),
            "--root",
            str(stage),
            "--gpu",
            "6",
            "--result-json",
            str(result_json),
        ]
        for spec in changed_specs:
            command.extend(["--task-id", spec.task_id])
        completed = subprocess.run(
            command,
            cwd=HERE,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        if completed.stdout:
            print(completed.stdout.rstrip(), flush=True)
        if completed.returncode != 0:
            raise RuntimeError(
                f"changed-comparison renderer exited {completed.returncode}"
            )
        rendered = json.loads(result_json.read_text(encoding="utf-8"))
        result_json.unlink()
        for task_id, areas in rendered.items():
            results[task_id] = {str(role): int(area) for role, area in areas.items()}

        pair_paths: list[Path] = []
        for spec in specs:
            matches = list((stage / "comparison_png").glob(f"{spec.task_id}__*.png"))
            if len(matches) != 1:
                raise RuntimeError(f"{spec.task_id}: contact-sheet PNG mismatch")
            pair_paths.append(matches[0])
        thumb_w, thumb_h, columns = 320, 238, 4
        rows = (len(pair_paths) + columns - 1) // columns
        sheet = Image.new("RGB", (columns * thumb_w, rows * thumb_h), "#e9e5dc")
        for index, path in enumerate(pair_paths):
            pair = Image.open(path).convert("RGB")
            pair.thumbnail((thumb_w - 8, thumb_h - 8), Image.Resampling.LANCZOS)
            x_value = (index % columns) * thumb_w + (thumb_w - pair.width) // 2
            y_value = (index // columns) * thumb_h + (thumb_h - pair.height) // 2
            sheet.paste(pair, (x_value, y_value))
        sheet.save(stage / "comparison_png/ALL_ANALOGY_CANDIDATES_CONTACT_SHEET.png")
    if len(results) != len(specs):
        raise RuntimeError(
            f"comparison area count mismatch: {len(results)} vs {len(specs)}"
        )
    print(
        f"Reused {len(specs) - len(changed_specs)} BDDL-matched comparison PNGs and "
        f"rerendered {len(changed_specs)} changed tasks from {source_root}",
        flush=True,
    )
    return results


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state-count", type=int, default=50)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument(
        "--parallel-init",
        action="store_true",
        help="generate unique physical groups concurrently on physical GPUs 6 and 7",
    )
    parser.add_argument(
        "--parallel-render",
        action="store_true",
        help="render comparison and exact-mask PNGs concurrently on physical GPUs 6 and 7",
    )
    parser.add_argument(
        "--reuse-comparisons-from",
        type=Path,
        help="reuse already-rendered PNGs after exact BDDL and nonempty-mask verification",
    )
    parser.add_argument(
        "--rerender-changed-comparisons",
        action="store_true",
        help="with --reuse-comparisons-from, rerender only tasks whose BDDL changed",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.state_count < 1:
        raise ValueError(args.state_count)
    if args.rerender_changed_comparisons and args.reuse_comparisons_from is None:
        raise ValueError("--rerender-changed-comparisons requires --reuse-comparisons-from")
    if OUTPUT_ROOT.exists() and not args.overwrite:
        raise FileExistsError(f"refusing to overwrite {OUTPUT_ROOT}")
    os.environ.setdefault("CUDA_VISIBLE_DEVICES", "6,7")
    os.environ.setdefault("MUJOCO_EGL_DEVICE_ID", "6")
    os.environ.setdefault("MUJOCO_GL", "egl")
    os.environ.setdefault("PYOPENGL_PLATFORM", "egl")

    specs = build_specs()
    stage_parent = Path(tempfile.mkdtemp(prefix=".LiberoAnalogyExpanded_", dir=HERE))
    stage = stage_parent / OUTPUT_ROOT.name
    stage.mkdir()
    try:
        bundles: dict[str, Path] = {}
        bddl_by_id: dict[str, str] = {}
        for spec in specs:
            text = base.base_transform(spec, spec.source_bddl.read_text(encoding="utf-8"))
            bddl_by_id[spec.task_id] = text
            bundles[spec.task_id] = base.write_task_bundle(stage, spec, text)
        if args.parallel_init:
            copy_or_generate_init_parallel(specs, bundles, bddl_by_id, args.state_count)
        else:
            base.copy_or_generate_init(specs, bundles, bddl_by_id, args.state_count)
        if args.reuse_comparisons_from is not None:
            mask_areas = reuse_validated_comparisons(
                specs,
                bundles,
                args.reuse_comparisons_from.resolve(),
                stage,
                rerender_changed=args.rerender_changed_comparisons,
            )
        elif args.parallel_render:
            mask_areas = render_comparisons_parallel(specs, stage)
        else:
            mask_areas = base.render_comparisons(specs, bundles, stage)
        (stage / "ANALOGY_RULES.md").write_text(rules_document(), encoding="utf-8")
        (stage / "REJECTED_CANDIDATES.tsv").write_text(
            "candidate\tinstruction\tsource\treason\n"
            "E3_REJECTED_SCENE8_BOWL_FROM\t"
            "Pick up the black bowl on the stove at the LIBERO-10 Scene 8 donor position and place it on the plate.\t"
            "libero_spatial/pick_up_the_black_bowl_on_the_stove_and_place_it_on_the_plate\t"
            "Simulator gate: no stable init state after repeated 1-state smoke attempts; other two bowl-from-stove donors and the Scene-8 bowl-to-stove goal remain.\n"
            "E4_REJECTED_SOUP_BASKET_KETCHUP_SLOT\t"
            "Put the alphabet soup in the basket at the former ketchup position.\t"
            "libero_10/LIVING_ROOM_SCENE1_put_both_the_alphabet_soup_and_the_cream_cheese_box_in_the_basket\t"
            "Simulator gate: 0 stable states across every reset attempt; the exact small-object donor slot is not stable for this basket/source-object combination.\n"
            "S4_REJECTED_BUTTER_ON_RAMEKIN\t"
            "Pick up the butter on the ramekin and place it on the plate.\t"
            "libero_spatial/pick_up_the_black_bowl_on_the_ramekin_and_place_it_on_the_plate\t"
            "Semantic init gate: after settling, butter no longer satisfies On(butter, ramekin); the pudding variant remains valid.\n",
            encoding="utf-8",
        )
        base.write_indexes(stage, specs, bundles, mask_areas)
        validate(stage, specs, bundles, args.state_count)

        # Correct the generic base README status/links with expansion-specific facts.
        readme = (stage / "README.md").read_text(encoding="utf-8")
        readme = readme.replace("# LIBERO Analogy candidate index", "# LIBERO Analogy Expanded: context-preserving scene lattice")
        readme = readme.replace("policy inference not run", "policy inference not run yet")
        (stage / "README.md").write_text(readme, encoding="utf-8")

        if OUTPUT_ROOT.exists():
            backup = HERE / f".{OUTPUT_ROOT.name}.old"
            if backup.exists():
                shutil.rmtree(backup)
            OUTPUT_ROOT.rename(backup)
            stage.rename(OUTPUT_ROOT)
            shutil.rmtree(backup)
        else:
            stage.rename(OUTPUT_ROOT)
        print(f"Built {len(specs)} clean expanded tasks at {OUTPUT_ROOT}", flush=True)
    finally:
        if stage_parent.exists():
            shutil.rmtree(stage_parent)


if __name__ == "__main__":
    main()
