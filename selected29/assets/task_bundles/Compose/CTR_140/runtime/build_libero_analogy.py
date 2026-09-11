#!/usr/bin/env python3
"""Build the single-skill LIBERO Analogy candidate pool.

The pool keeps the learned object identity and action/relation template while
changing one structural binding: a seen interaction position, an exact target
instance, a sibling drawer slot, or a reference fixture pose.  The generated
tasks are definitions only; this script does not run policy inference.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import os
import pickle
import re
import shutil
import sys
import tempfile
import textwrap
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

import numpy as np
import yaml
from PIL import Image, ImageDraw, ImageFont


HERE = Path(__file__).resolve().parent
OUTPUT_ROOT = HERE / "LiberoAnalogy"
LIBERO_ROOT = Path(
    "/path/to/local_runtime/CORL26/third_party/Isaac-GR00T/"
    "external_dependencies/LIBERO/libero/libero"
)
SCRIPT_ROOT = Path("/path/to/local_runtime/CORL26/LiberoEX_final/scripts")
POSITION_SWAP_ROOT = HERE / "LiberoFinalObj/PositionSwap"

SOURCE_BDDL = LIBERO_ROOT / "bddl_files"
SOURCE_INIT = LIBERO_ROOT / "init_files"
ORIGINAL_REVIEW = HERE / "LiberoOriginal40Review"

GOAL = SOURCE_BDDL / "libero_goal"
GOAL_INIT = SOURCE_INIT / "libero_goal"
SPATIAL = SOURCE_BDDL / "libero_spatial"
SPATIAL_INIT = SOURCE_INIT / "libero_spatial"
LIBERO10 = SOURCE_BDDL / "libero_10"
LIBERO10_INIT = SOURCE_INIT / "libero_10"

GOAL_COMMON = GOAL / "turn_on_the_stove.bddl"
GOAL_COMMON_INIT = GOAL_INIT / "turn_on_the_stove.pruned_init"
GOAL_PUSH = GOAL / "push_the_plate_to_the_front_of_the_stove.bddl"
GOAL_PUSH_INIT = GOAL_INIT / "push_the_plate_to_the_front_of_the_stove.pruned_init"
GOAL_BOWL_STOVE = GOAL / "put_the_bowl_on_the_stove.bddl"
GOAL_BOWL_STOVE_INIT = GOAL_INIT / "put_the_bowl_on_the_stove.pruned_init"
GOAL_DRAWER_TOP = GOAL / "open_the_top_drawer_and_put_the_bowl_inside.bddl"
GOAL_DRAWER_TOP_INIT = GOAL_INIT / "open_the_top_drawer_and_put_the_bowl_inside.pruned_init"
GOAL_DRAWER_MIDDLE = GOAL / "open_the_middle_drawer_of_the_cabinet.bddl"
GOAL_DRAWER_MIDDLE_INIT = GOAL_INIT / "open_the_middle_drawer_of_the_cabinet.pruned_init"

SCENE5 = LIBERO10 / "LIVING_ROOM_SCENE5_put_the_white_mug_on_the_left_plate_and_put_the_yellow_and_white_mug_on_the_right_plate.bddl"
SCENE5_INIT = LIBERO10_INIT / "LIVING_ROOM_SCENE5_put_the_white_mug_on_the_left_plate_and_put_the_yellow_and_white_mug_on_the_right_plate.pruned_init"
KITCHEN4 = LIBERO10 / "KITCHEN_SCENE4_put_the_black_bowl_in_the_bottom_drawer_of_the_cabinet_and_close_it.bddl"
KITCHEN4_INIT = LIBERO10_INIT / "KITCHEN_SCENE4_put_the_black_bowl_in_the_bottom_drawer_of_the_cabinet_and_close_it.pruned_init"
SCENE1 = LIBERO10 / "LIVING_ROOM_SCENE1_put_both_the_alphabet_soup_and_the_cream_cheese_box_in_the_basket.bddl"
SCENE1_INIT = LIBERO10_INIT / "LIVING_ROOM_SCENE1_put_both_the_alphabet_soup_and_the_cream_cheese_box_in_the_basket.pruned_init"
STUDY1 = LIBERO10 / "STUDY_SCENE1_pick_up_the_book_and_place_it_in_the_back_compartment_of_the_caddy.bddl"
STUDY1_INIT = LIBERO10_INIT / "STUDY_SCENE1_pick_up_the_book_and_place_it_in_the_back_compartment_of_the_caddy.pruned_init"
KITCHEN6 = LIBERO10 / "KITCHEN_SCENE6_put_the_yellow_and_white_mug_in_the_microwave_and_close_it.bddl"
KITCHEN6_INIT = LIBERO10_INIT / "KITCHEN_SCENE6_put_the_yellow_and_white_mug_in_the_microwave_and_close_it.pruned_init"
SPATIAL_STOVE = SPATIAL / "pick_up_the_black_bowl_on_the_stove_and_place_it_on_the_plate.bddl"
SPATIAL_STOVE_INIT = SPATIAL_INIT / "pick_up_the_black_bowl_on_the_stove_and_place_it_on_the_plate.pruned_init"

DUMMY_ACTION = np.zeros(7, dtype=np.float32)


@dataclass
class MaskSelector:
    role: str
    kind: str
    value: str
    color: str
    exact_instance: bool = True


@dataclass
class Spec:
    task_id: str
    family: str
    language: str
    source_bddl: Path
    source_init: Path
    source_instruction: str
    source_suite: str
    source_task_id: int | None
    goal_atom: str
    goal_bddl: str
    objects_of_interest: list[str]
    action_plan: list[dict[str, Any]]
    masks: list[MaskSelector]
    transform: Callable[[str], str]
    varied: list[str]
    held_fixed: list[str]
    critical_objects: list[str]
    physical_group: str
    notes: list[str] = field(default_factory=list)
    copied_from: Path | None = None


def load_yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def dump_yaml(path: Path, value: Any) -> None:
    path.write_text(
        yaml.safe_dump(value, sort_keys=False, allow_unicode=True, width=1200),
        encoding="utf-8",
    )


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replace_language(text: str, language: str) -> str:
    output, count = re.subn(
        r"(?m)^(\s*\(:language\s+).*(\)\s*)$",
        rf"\g<1>{language}\g<2>",
        text,
        count=1,
    )
    if count != 1:
        raise ValueError("language replacement failed")
    return output


def replace_section(text: str, section: str, next_section: str, replacement: str) -> str:
    pattern = rf"^[ \t]*\(:{section}\n.*?^[ \t]*\)\n\n[ \t]*\(:{next_section}"
    output, count = re.subn(
        pattern,
        replacement + f"\n\n  (:{next_section}",
        text,
        count=1,
        flags=re.DOTALL | re.MULTILINE,
    )
    if count != 1:
        raise ValueError(f"section replacement failed: {section}")
    return output


def replace_interest(text: str, names: list[str]) -> str:
    body = "\n".join(f"    {name}" for name in names)
    return replace_section(text, "obj_of_interest", "init", f"  (:obj_of_interest\n{body}\n  )")


def replace_goal(text: str, goal_bddl: str) -> str:
    output, count = re.subn(
        r"  \(:goal\n.*?\n  \)\n\n\)",
        f"  (:goal\n    (And {goal_bddl})\n  )\n\n)",
        text,
        count=1,
        flags=re.DOTALL,
    )
    if count != 1:
        raise ValueError("goal replacement failed")
    return output


def replace_region_range(
    text: str,
    region_name: str,
    ranges: tuple[float, float, float, float],
) -> str:
    vals = " ".join(str(value) for value in ranges)
    pattern = rf"(\({re.escape(region_name)}\s+\(:target\s+[^)]+\)\s+\(:ranges\s*\(\s*\()[^)]*(\))"
    output, count = re.subn(pattern, rf"\g<1>{vals}\g<2>", text, count=1, flags=re.DOTALL)
    if count != 1:
        raise ValueError(f"region replacement failed: {region_name}")
    return output


def replace_region_yaw(text: str, region_name: str, yaw: float) -> str:
    pattern = rf"(\({re.escape(region_name)}\s+\(:target\s+[^)]+\).*?\(:yaw_rotation\s*\(\s*\()[^)]*(\))"
    output, count = re.subn(
        pattern,
        rf"\g<1>{yaw} {yaw}\g<2>",
        text,
        count=1,
        flags=re.DOTALL,
    )
    if count != 1:
        raise ValueError(f"yaw replacement failed: {region_name}")
    return output


def add_region_before_fixtures(text: str, block: str) -> str:
    marker = "\n    )\n\n  (:fixtures"
    if marker not in text:
        raise ValueError("regions/fixtures boundary not found")
    return text.replace(marker, "\n" + block.rstrip() + marker, 1)


def replace_open_init(text: str, fixture: str, slot: str) -> str:
    output, count = re.subn(
        rf"\(Open\s+{re.escape(fixture)}_(?:top|middle|bottom)_region\)",
        f"(Open {fixture}_{slot}_region)",
        text,
        count=1,
    )
    if count == 0:
        marker = "\n  )\n\n  (:goal"
        if marker not in output:
            raise ValueError("init/goal boundary not found")
        output = output.replace(
            marker,
            f"\n    (Open {fixture}_{slot}_region)" + marker,
            1,
        )
    return output


def base_transform(spec: Spec, text: str) -> str:
    text = spec.transform(text)
    text = replace_language(text, spec.language)
    text = replace_interest(text, spec.objects_of_interest)
    text = replace_goal(text, spec.goal_bddl)
    return text


def action(action_type: str, primary: str, target: str, source_id: int | None, desc: str) -> dict[str, Any]:
    return {
        "action_type": action_type,
        "primary_object_id": primary,
        "target_object_id": target,
        "source_task_id": source_id,
        "source_task_description": desc,
    }


def pick_place(obj: str, target: str, source_id: int | None, desc: str) -> list[dict[str, Any]]:
    return [
        action("grasp", obj, obj, source_id, desc),
        action("release", obj, target, source_id, desc),
    ]


def parse_language(path: Path) -> str:
    match = re.search(r"\(:language\s+(.*?)\)", path.read_text(encoding="utf-8"))
    if not match:
        raise ValueError(path)
    return match.group(1).strip()


def identity(text: str) -> str:
    return text


def triple_plate(text: str) -> str:
    block = """      (plate_middle_region
          (:target living_room_table)
          (:ranges (
              (0.075 -0.025 0.125 0.025)
            )
          )
          (:yaw_rotation (
              (0.0 0.0)
            )
          )
      )"""
    text = add_region_before_fixtures(text, block)
    text, count = re.subn(r"plate_1\s+plate_2\s+-\s+plate", "plate_1 plate_2 plate_3 - plate", text, count=1)
    if count != 1:
        raise ValueError("plate declaration replacement failed")
    marker = "    (On plate_2 living_room_table_plate_right_region)"
    if marker not in text:
        raise ValueError("plate_2 init not found")
    text = text.replace(marker, marker + "\n    (On plate_3 living_room_table_plate_middle_region)", 1)
    return text


def white_drawer(slot: str) -> Callable[[str], str]:
    return lambda text: replace_open_init(text, "white_cabinet_1", slot)


def wooden_drawer(slot: str) -> Callable[[str], str]:
    return lambda text: replace_open_init(text, "wooden_cabinet_1", slot)


def relocated_cabinet(text: str) -> str:
    text = replace_region_range(text, "cabinet_region", (0.02, 0.23, 0.04, 0.25))
    # The cabinet crosses to the opposite side of the tabletop.  Rotate it so
    # the drawer front/handles remain camera-visible and arm-facing.
    return replace_region_yaw(text, "cabinet_region", 0.0)


def relocated_goal_stove(text: str) -> str:
    text = replace_region_range(text, "stove_region", (-0.42, -0.15, -0.4, -0.13))
    if "(stove_front_region" in text:
        text = replace_region_range(text, "stove_front_region", (-0.09, -0.18, -0.01, -0.10))
    return text


def relocated_spatial_stove(text: str) -> str:
    return replace_region_range(text, "stove_region", (-0.42, 0.20, -0.4, 0.22))


def relocated_basket(text: str) -> str:
    # Back-left slot: fully visible and separated from all movable objects.
    return replace_region_range(text, "basket_init_region", (-0.19, 0.17, -0.17, 0.19))


def relocated_caddy(text: str) -> str:
    # Mirror laterally while retaining the original depth / arm distance.
    return replace_region_range(text, "desk_caddy_init_region", (-0.21, 0.13, -0.19, 0.15))


def relocated_microwave(text: str) -> str:
    # Back-right-adjacent slot with the complete fixture inside the camera.
    return replace_region_range(text, "microwave_init_region", (-0.19, 0.14, -0.17, 0.16))


def selector(role: str, kind: str, value: str, color: str) -> MaskSelector:
    # Keep review colors and stove-control scope consistent across every
    # generated benchmark. Articulated controls are cyan, and stove turning
    # exposes only the rotary button rather than the complete appliance.
    if role.startswith("interaction"):
        color = "cyan"
        if kind == "body_prefix" and value == "flat_stove_1":
            value = "flat_stove_1_button"
    return MaskSelector(role=role, kind=kind, value=value, color=color)


def original_masked_scene(bddl_path: Path) -> np.ndarray:
    """Load the exact-mask init-state image for an original LIBERO-40 task."""
    index_path = ORIGINAL_REVIEW / "TASK_INDEX.tsv"
    if not index_path.is_file():
        raise FileNotFoundError(index_path)
    target_name = bddl_path.name
    with index_path.open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    matches = [
        row
        for row in rows
        if Path(str(row["bddl_path"]).replace("libero://", "/")).name == target_name
    ]
    if len(matches) != 1:
        raise RuntimeError(
            f"expected one original LIBERO-40 mask image for {target_name}, found {len(matches)}"
        )
    path = ORIGINAL_REVIEW / "masked_scenes" / matches[0]["raw_png"]
    if not path.is_file():
        raise FileNotFoundError(path)
    return np.asarray(Image.open(path).convert("RGB"))


def build_position_specs() -> list[Spec]:
    specs: list[Spec] = []
    source_ids = {
        "alphabet_soup": 301,
        "cream_cheese": 302,
        "salad_dressing": 303,
        "bbq_sauce": 304,
        "ketchup": 305,
        "tomato_sauce": 306,
        "butter": 307,
        "milk": 308,
        "chocolate_pudding": 309,
        "orange_juice": 310,
    }
    for index, bundle in enumerate(sorted(POSITION_SWAP_ROOT.glob("ogts_*")), start=1):
        meta = load_yaml(bundle / "task_meta.yaml")
        target = str(meta["source_target_object"])
        stem = str(meta["source_prior_task_stem"])
        source_bddl = SOURCE_BDDL / "libero_object" / f"{stem}.bddl"
        source_init = SOURCE_INIT / "libero_object" / f"{stem}.pruned_init"
        task_id = f"ANLG_{index:03d}"
        target_type = target.removesuffix("_1")
        language = str(meta["language"])
        specs.append(
            Spec(
                task_id=task_id,
                family="A1_same_object_seen_position_transfer",
                language=language,
                source_bddl=source_bddl,
                source_init=source_init,
                source_instruction=parse_language(source_bddl),
                source_suite="libero_object",
                source_task_id=source_ids[target_type],
                goal_atom=f"in({target}, basket_1_contain_region)",
                goal_bddl=f"(In {target} basket_1_contain_region)",
                objects_of_interest=[target, "basket_1"],
                action_plan=pick_place(target, "basket_1_contain_region", source_ids[target_type], language),
                masks=[
                    selector("manipulated_object", "body_prefix", target, "green"),
                    selector("goal_target", "body_prefix", "basket_1", "yellow"),
                ],
                transform=identity,
                varied=list(meta.get("varied") or []),
                held_fixed=list(meta.get("held_fixed") or []),
                critical_objects=[target, "basket_1"],
                physical_group=task_id,
                notes=[
                    "Target is moved only to the other pose used as a target-grasp pose in original LIBERO-Object.",
                    f"Legacy position-swap provenance: {meta.get('source_legacy_task_id')}",
                ],
                copied_from=bundle,
            )
        )
    return specs


def build_custom_specs() -> list[Spec]:
    specs: list[Spec] = []

    plate_rows = [
        (11, "Put the white mug on the middle plate.", "porcelain_mug_1", "plate_3", "middle"),
        (12, "Put the white mug on the right plate.", "porcelain_mug_1", "plate_2", "right"),
        (13, "Put the yellow and white mug on the left plate.", "white_yellow_mug_1", "plate_1", "left"),
        (14, "Put the yellow and white mug on the middle plate.", "white_yellow_mug_1", "plate_3", "middle"),
    ]
    for idx, language, obj, plate, plate_label in plate_rows:
        specs.append(
            Spec(
                task_id=f"ANLG_{idx:03d}",
                family="A2_exact_instance_binding_three_plates",
                language=language,
                source_bddl=SCENE5,
                source_init=SCENE5_INIT,
                source_instruction=parse_language(SCENE5),
                source_suite="libero_10",
                source_task_id=104,
                goal_atom=f"on({obj}, {plate})",
                goal_bddl=f"(On {obj} {plate})",
                objects_of_interest=[obj, plate],
                action_plan=pick_place(obj, plate, 104, language),
                masks=[
                    selector("manipulated_object", "body_prefix", obj, "green"),
                    selector("goal_target", "body_prefix", plate, "yellow"),
                ],
                transform=triple_plate,
                varied=[
                    "add one plate at the center slot",
                    f"bind the instruction to the exact {plate_label} plate instance ({plate})",
                ],
                held_fixed=[
                    "source mug identities and spawn regions",
                    "source left and right plate poses",
                    "single On relation template",
                ],
                critical_objects=["porcelain_mug_1", "white_yellow_mug_1", "plate_1", "plate_2", "plate_3"],
                physical_group="three_plate_scene5",
                notes=["The target mask must contain only the instructed plate instance; plate masks must never be unioned."],
            )
        )

    drawer_rows = [
        (15, KITCHEN4, KITCHEN4_INIT, 103, "white_cabinet_1", "middle", white_drawer("middle"), "Put the black bowl in the middle drawer of the cabinet.", "white_middle"),
        (16, KITCHEN4, KITCHEN4_INIT, 103, "white_cabinet_1", "top", white_drawer("top"), "Put the black bowl in the top drawer of the cabinet.", "white_top"),
        (17, GOAL_DRAWER_TOP, GOAL_DRAWER_TOP_INIT, 3, "wooden_cabinet_1", "middle", wooden_drawer("middle"), "Put the black bowl in the middle drawer of the wooden cabinet.", "wooden_middle"),
        (18, GOAL_DRAWER_TOP, GOAL_DRAWER_TOP_INIT, 3, "wooden_cabinet_1", "bottom", wooden_drawer("bottom"), "Put the black bowl in the bottom drawer of the wooden cabinet.", "wooden_bottom"),
    ]
    for idx, source_bddl, source_init, source_id, fixture, slot, transform, language, group in drawer_rows:
        target = f"{fixture}_{slot}_region"
        specs.append(
            Spec(
                task_id=f"ANLG_{idx:03d}",
                family="A3_sibling_drawer_slot_transfer",
                language=language,
                source_bddl=source_bddl,
                source_init=source_init,
                source_instruction=parse_language(source_bddl),
                source_suite="libero_10" if fixture.startswith("white") else "libero_goal",
                source_task_id=source_id,
                goal_atom=f"in(akita_black_bowl_1, {target})",
                goal_bddl=f"(In akita_black_bowl_1 {target})",
                objects_of_interest=["akita_black_bowl_1", target],
                action_plan=pick_place("akita_black_bowl_1", target, source_id, language),
                masks=[
                    selector("manipulated_object", "body_prefix", "akita_black_bowl_1", "green"),
                    selector("goal_target", "drawer_part", f"{fixture}:{slot}", "yellow"),
                ],
                transform=transform,
                varied=[f"transfer the learned drawer insertion relation to the {slot} sibling slot"],
                held_fixed=[
                    "source cabinet pose and type",
                    "black bowl identity and spawn family",
                    "target drawer is initialized open to isolate the single insertion relation",
                ],
                critical_objects=["akita_black_bowl_1", fixture],
                physical_group=group,
                notes=["No Close goal is included; this is one semantic goal atom."],
            )
        )

    relocate_drawer_rows = [
        (19, GOAL_DRAWER_MIDDLE, GOAL_DRAWER_MIDDLE_INIT, 10, "middle", "Open the middle drawer of the relocated wooden cabinet."),
        (20, GOAL_DRAWER_TOP, GOAL_DRAWER_TOP_INIT, 3, "top", "Open the top drawer of the relocated wooden cabinet."),
    ]
    for idx, source_bddl, source_init, source_id, slot, language in relocate_drawer_rows:
        target = f"wooden_cabinet_1_{slot}_region"
        specs.append(
            Spec(
                task_id=f"ANLG_{idx:03d}",
                family="A4_articulated_fixture_pose_transfer",
                language=language,
                source_bddl=source_bddl,
                source_init=source_init,
                source_instruction=parse_language(source_bddl),
                source_suite="libero_goal",
                source_task_id=source_id,
                goal_atom=f"open({target})",
                goal_bddl=f"(Open {target})",
                objects_of_interest=[target],
                action_plan=[action("open", target, target, source_id, language)],
                masks=[selector("interaction_target", "drawer_part", f"wooden_cabinet_1:{slot}", "green")],
                transform=relocated_cabinet,
                varied=["move wooden cabinet from (0.03, -0.24, yaw=pi) to (0.03, +0.24, yaw=0) so its front remains arm-facing"],
                held_fixed=["cabinet type", "drawer slot identity", "single Open predicate", "all other source objects and fixture poses"],
                critical_objects=["wooden_cabinet_1"],
                physical_group="relocated_wooden_cabinet",
            )
        )

    stove_rows = [
        (21, GOAL_COMMON, GOAL_COMMON_INIT, 7, "Turn on the relocated stove.", "turnon(flat_stove_1)", "(Turnon flat_stove_1)", ["flat_stove_1"], [action("turn_on", "flat_stove_1", "flat_stove_1", 7, "Turn on the stove")], [selector("interaction_target", "body_prefix", "flat_stove_1", "green")], ["flat_stove_1"]),
        (22, GOAL_PUSH, GOAL_PUSH_INIT, 6, "Push the plate to the front of the relocated stove.", "on(plate_1, main_table_stove_front_region)", "(On plate_1 main_table_stove_front_region)", ["plate_1", "main_table_stove_front_region"], [action("push", "plate_1", "main_table_stove_front_region", 6, "Push the plate to the front of the stove")], [selector("manipulated_object", "body_prefix", "plate_1", "green"), selector("goal_target", "table_region", "main_table_stove_front_region", "yellow")], ["plate_1", "flat_stove_1"]),
        (23, GOAL_BOWL_STOVE, GOAL_BOWL_STOVE_INIT, 8, "Put the black bowl on the relocated stove.", "on(akita_black_bowl_1, flat_stove_1_cook_region)", "(On akita_black_bowl_1 flat_stove_1_cook_region)", ["akita_black_bowl_1", "flat_stove_1_cook_region"], pick_place("akita_black_bowl_1", "flat_stove_1_cook_region", 8, "Put the bowl on the stove"), [selector("manipulated_object", "body_prefix", "akita_black_bowl_1", "green"), selector("goal_target", "body_prefix", "flat_stove_1", "yellow")], ["akita_black_bowl_1", "flat_stove_1"]),
    ]
    for idx, source_bddl, source_init, source_id, language, atom_text, goal, interest, plan, masks, critical in stove_rows:
        specs.append(
            Spec(
                task_id=f"ANLG_{idx:03d}",
                family="A5_reference_relative_stove_transfer",
                language=language,
                source_bddl=source_bddl,
                source_init=source_init,
                source_instruction=parse_language(source_bddl),
                source_suite="libero_goal",
                source_task_id=source_id,
                goal_atom=atom_text,
                goal_bddl=goal,
                objects_of_interest=interest,
                action_plan=plan,
                masks=masks,
                transform=relocated_goal_stove,
                varied=["move stove from main-table y=+0.21 to the LIBERO-Spatial donor y=-0.14", "translate stove-front region by the same y offset when applicable"],
                held_fixed=["stove type and yaw", "source object identities and all non-stove poses", "single learned predicate/relation"],
                critical_objects=critical,
                physical_group="relocated_goal_stove",
                notes=["For the push task, the placement mask is projected from the relocated BDDL stove_front_region, never the source absolute region."],
            )
        )

    specs.append(
        Spec(
            task_id="ANLG_024",
            family="A5_reference_relative_stove_transfer",
            language="Pick up the black bowl on the relocated stove and place it on the plate.",
            source_bddl=SPATIAL_STOVE,
            source_init=SPATIAL_STOVE_INIT,
            source_instruction=parse_language(SPATIAL_STOVE),
            source_suite="libero_spatial",
            source_task_id=None,
            goal_atom="on(akita_black_bowl_1, plate_1)",
            goal_bddl="(On akita_black_bowl_1 plate_1)",
            objects_of_interest=["akita_black_bowl_1", "plate_1"],
            action_plan=pick_place("akita_black_bowl_1", "plate_1", None, "Pick up the black bowl on the stove and place it on the plate"),
            masks=[selector("manipulated_object", "body_prefix", "akita_black_bowl_1", "green"), selector("goal_target", "body_prefix", "plate_1", "yellow")],
            transform=relocated_spatial_stove,
            varied=["move stove and the bowl initialized on it from y=-0.14 to the LIBERO-Goal stove pose y=+0.21"],
            held_fixed=["spatial source scene, object set, plate pose, stove type", "single bowl-to-plate relation"],
            critical_objects=["akita_black_bowl_1", "plate_1", "flat_stove_1"],
            physical_group="relocated_spatial_stove",
        )
    )

    receptacle_rows = [
        (25, "A6_receptacle_pose_transfer", SCENE1, SCENE1_INIT, 107, "libero_10", "Put the alphabet soup in the relocated basket.", "alphabet_soup_1", "basket_1_contain_region", "in(alphabet_soup_1, basket_1_contain_region)", "(In alphabet_soup_1 basket_1_contain_region)", relocated_basket, "basket_1", "relocated_basket_scene1"),
        (26, "A6_receptacle_pose_transfer", STUDY1, STUDY1_INIT, 105, "libero_10", "Put the book in the back compartment of the relocated desk caddy.", "black_book_1", "desk_caddy_1_back_contain_region", "in(black_book_1, desk_caddy_1_back_contain_region)", "(In black_book_1 desk_caddy_1_back_contain_region)", relocated_caddy, "desk_caddy_1", "relocated_caddy_study1"),
        (27, "A6_receptacle_pose_transfer", KITCHEN6, KITCHEN6_INIT, 109, "libero_10", "Put the yellow and white mug in the relocated microwave.", "white_yellow_mug_1", "microwave_1_heating_region", "in(white_yellow_mug_1, microwave_1_heating_region)", "(In white_yellow_mug_1 microwave_1_heating_region)", relocated_microwave, "microwave_1", "relocated_microwave_kitchen6"),
    ]
    for idx, family, source_bddl, source_init, source_id, suite, language, obj, target, atom_text, goal, transform, fixture, group in receptacle_rows:
        specs.append(
            Spec(
                task_id=f"ANLG_{idx:03d}",
                family=family,
                language=language,
                source_bddl=source_bddl,
                source_init=source_init,
                source_instruction=parse_language(source_bddl),
                source_suite=suite,
                source_task_id=source_id,
                goal_atom=atom_text,
                goal_bddl=goal,
                objects_of_interest=[obj, target],
                action_plan=pick_place(obj, target, source_id, language),
                masks=[selector("manipulated_object", "body_prefix", obj, "green"), selector("goal_target", "body_prefix", fixture, "yellow")],
                transform=transform,
                varied=[f"relocate {fixture} to a collision-free mirrored/adjacent reachable slot on the same source table"],
                held_fixed=["source object identity and spawn", "receptacle type and local containment geometry", "single learned In relation", "all non-receptacle source poses"],
                # Packaged objects and large receptacles can settle with
                # harmless yaw changes that exceed the generic 18-degree gate.
                # These layouts are instead gated by successful reset,
                # non-initial success, and exact non-empty masks at render time.
                critical_objects=[],
                physical_group=group,
            )
        )

    return specs


def build_specs() -> list[Spec]:
    specs = build_position_specs() + build_custom_specs()
    assert [spec.task_id for spec in specs] == [f"ANLG_{idx:03d}" for idx in range(1, 28)]
    assert len({spec.task_id for spec in specs}) == 27
    return specs


def import_scaffold_helpers():
    sys.path.insert(0, str(SCRIPT_ROOT))
    import generate_libero10_generalization_scaffolds as base

    return base


def patch_robosuite_segmentation_uint8_overflow() -> None:
    """Make legacy robosuite segmentation compatible with NumPy 2.x.

    The bundled reader multiplies uint8 channels by 256/65536 before casting,
    which NumPy 2 rejects.  Keep the same implementation but cast to int32
    first.  This is process-local and does not edit the installed package.
    """
    import mujoco
    from robosuite.utils import binding_utils

    cls = binding_utils.MjRenderContextOffscreen
    if getattr(cls.read_pixels, "_libero_analogy_uint8_patch", False):
        return
    original = cls.read_pixels

    def patched(self, width, height, depth=False, segmentation=False):
        if not segmentation:
            return original(self, width, height, depth=depth, segmentation=False)
        viewport = mujoco.MjrRect(0, 0, width, height)
        rgb_img = np.empty((height, width, 3), dtype=np.uint8)
        depth_img = np.empty((height, width), dtype=np.float32) if depth else None
        mujoco.mjr_readPixels(rgb=rgb_img, depth=depth_img, viewport=viewport, con=self.con)
        channels = rgb_img.astype(np.int32)
        seg_img = channels[:, :, 0] + channels[:, :, 1] * 256 + channels[:, :, 2] * 65536
        seg_img[seg_img >= (self.scn.ngeom + 1)] = 0
        seg_ids = np.full((self.scn.ngeom + 1, 2), fill_value=-1, dtype=np.int32)
        for index in range(self.scn.ngeom):
            geom = self.scn.geoms[index]
            if geom.segid != -1:
                seg_ids[geom.segid + 1, 0] = geom.objtype
                seg_ids[geom.segid + 1, 1] = geom.objid
        result = seg_ids[seg_img]
        return (result, depth_img) if depth else result

    patched._libero_analogy_uint8_patch = True  # type: ignore[attr-defined]
    cls.read_pixels = patched


def save_init_array(path: Path, array: np.ndarray) -> None:
    payload = pickle.dumps(np.asarray(array), protocol=2)
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_STORED) as archive:
        archive.writestr("archive/data.pkl", payload)
        archive.writestr("archive/version", "3\n")


def load_init_array(path: Path) -> np.ndarray:
    with zipfile.ZipFile(path, "r") as archive:
        name = next(value for value in archive.namelist() if value.endswith("data.pkl"))
        return np.asarray(pickle.loads(archive.read(name)))


def write_task_bundle(root: Path, spec: Spec, bddl_text: str) -> Path:
    slug = f"{spec.task_id.lower()}__{slugify(spec.language)}"
    bundle = root / "tasks" / slug
    bundle.mkdir(parents=True)
    (bundle / "task.bddl").write_text(bddl_text, encoding="utf-8")
    canonical_signature = f"analogy|{spec.family}|{spec.physical_group}|{spec.goal_atom}"
    metadata = {
        "task_id": spec.task_id,
        "task_name": spec.language,
        "language": spec.language,
        "primary_category": "Analogy",
        "analogy_family": spec.family,
        "anchor_suite": spec.source_suite,
        "source_prior_task_ids": [] if spec.source_task_id is None else [spec.source_task_id],
        "source_prior_task_stem": spec.source_bddl.stem,
        "source_prior_description": spec.source_instruction,
        "canonical_goal_atoms": [spec.goal_atom],
        "canonical_task_signature": canonical_signature,
        "objects_of_interest": spec.objects_of_interest,
        "held_fixed": spec.held_fixed,
        "varied": spec.varied,
        "single_semantic_goal": True,
        "physical_group": spec.physical_group,
        "base_bddl_template": str(spec.source_bddl),
        "base_pruned_init": str(spec.source_init),
        "definition_status": "defined_not_evaluated",
        "notes": spec.notes,
    }
    rules = {
        "task_id": spec.task_id,
        "category": "Analogy",
        "required_goal_atoms": [spec.goal_atom],
        "forbidden_goal_atoms": [],
        "order_sensitive": False,
        "continue_after_success": False,
        "requires_transition": False,
        "custom_eval_needed": False,
    }
    registry = {
        "name": spec.task_id,
        "language": spec.language,
        "problem": "Libero",
        "problem_folder": f"tasks/{slug}",
        "bddl_file": "task.bddl",
        "init_states_file": "task.pruned_init",
        "category": "Analogy",
        "anchor_suite": spec.source_suite,
        "metadata_file": "task_meta.yaml",
        "eval_rules_file": "eval_rules.yaml",
        "mask_bindings_file": "mask_bindings.yaml",
        "action_plan_file": "action_plan.yaml",
        "canonical_task_signature": canonical_signature,
    }
    mask_bindings = {
        "task_id": spec.task_id,
        "policy": "exact_instance_no_union",
        "bindings": [vars(value) for value in spec.masks],
        "runtime_requirements": {
            "resolve_by_current_sim_model": True,
            "allow_source_episode_json_fallback": False,
            "new_instance_support": any(value.value == "plate_3" for value in spec.masks),
            "region_projection_from_current_bddl": any(value.kind == "table_region" for value in spec.masks),
        },
    }
    dump_yaml(bundle / "task_meta.yaml", metadata)
    dump_yaml(bundle / "eval_rules.yaml", rules)
    dump_yaml(bundle / "registry_entry.yaml", registry)
    dump_yaml(bundle / "mask_bindings.yaml", mask_bindings)
    dump_yaml(bundle / "action_plan.yaml", {"task_id": spec.task_id, "steps": spec.action_plan})
    return bundle


def copy_or_generate_init(
    specs: list[Spec],
    bundles: dict[str, Path],
    bddl_by_id: dict[str, str],
    state_count: int,
) -> None:
    base = import_scaffold_helpers()
    os.environ["CUDA_VISIBLE_DEVICES"] = os.environ.get("CUDA_VISIBLE_DEVICES", "6,7")
    os.environ["MUJOCO_EGL_DEVICE_ID"] = os.environ.get("MUJOCO_EGL_DEVICE_ID", "6")
    os.environ["MUJOCO_GL"] = "egl"
    os.environ["PYOPENGL_PLATFORM"] = "egl"
    os.environ["LIBERO_EX_MAX_INIT_STATES"] = str(state_count)
    os.environ.setdefault("LIBERO_EX_MAX_TASK_SECONDS", "1800")

    generated_group_path: dict[str, Path] = {}
    cache_root = HERE / ".LiberoAnalogy_state_cache"
    cache_root.mkdir(exist_ok=True)
    OffScreenRenderEnv = None
    total = len(specs)
    for index, spec in enumerate(specs, start=1):
        destination = bundles[spec.task_id] / "task.pruned_init"
        if spec.copied_from is not None:
            copied = load_init_array(spec.copied_from / "task.pruned_init")
            if len(copied) < state_count:
                raise RuntimeError(
                    f"{spec.task_id}: copied source has {len(copied)} states, expected at least {state_count}"
                )
            save_init_array(destination, copied[:state_count])
            print(f"[{index:03d}/{total}] {spec.task_id}: copied validated position-swap states", flush=True)
            continue
        if spec.physical_group in generated_group_path:
            shutil.copy2(generated_group_path[spec.physical_group], destination)
            print(f"[{index:03d}/{total}] {spec.task_id}: reused physical group {spec.physical_group}", flush=True)
            continue
        cache_key = hashlib.sha256(
            (
                bddl_by_id[spec.task_id]
                + f"\nstate_count={state_count}"
                + f"\ncritical={','.join(spec.critical_objects)}"
            ).encode("utf-8")
        ).hexdigest()[:20]
        cache_path = cache_root / f"{spec.physical_group}__{cache_key}.pruned_init"
        if cache_path.is_file():
            cached = load_init_array(cache_path)
            if len(cached) == state_count:
                shutil.copy2(cache_path, destination)
                generated_group_path[spec.physical_group] = destination
                print(f"[{index:03d}/{total}] {spec.task_id}: restored {state_count} states from hash cache", flush=True)
                continue
        if OffScreenRenderEnv is None:
            base.ensure_runtime_env()
            base.disable_interactive_pdb()
            OffScreenRenderEnv = base.load_env_cls()
        states = base.generate_init_states(
            OffScreenRenderEnv,
            bddl_path=bundles[spec.task_id] / "task.bddl",
            source_init_path=spec.source_init,
            critical_objects=spec.critical_objects,
            seed_base=310_000 + index * 1_000,
        )
        if len(states) != state_count:
            raise RuntimeError(f"{spec.task_id}: generated {len(states)} states, expected {state_count}")
        save_init_array(destination, states)
        shutil.copy2(destination, cache_path)
        generated_group_path[spec.physical_group] = destination
        print(f"[{index:03d}/{total}] {spec.task_id}: generated {len(states)} stable states", flush=True)


def load_font(size: int, bold: bool = False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    path = Path("/usr/share/fonts/truetype/dejavu") / name
    try:
        return ImageFont.truetype(str(path), size=size)
    except OSError:
        return ImageFont.load_default()


def fit_lines(draw: ImageDraw.ImageDraw, text: str, font, width: int) -> list[str]:
    words = str(text).split()
    if not words:
        return [""]
    lines: list[str] = []
    current = words[0]
    for word in words[1:]:
        candidate = f"{current} {word}"
        if draw.textbbox((0, 0), candidate, font=font)[2] <= width:
            current = candidate
        else:
            lines.append(current)
            current = word
    lines.append(current)
    return lines


def model_body_names(env) -> list[str]:
    return [str(env.sim.model.body_id2name(index) or "") for index in range(env.sim.model.nbody)]


def descendant_bodies(env, roots: set[int]) -> set[int]:
    parents = np.asarray(env.sim.model.body_parentid, dtype=np.int32)
    bodies = set(roots)
    changed = True
    while changed:
        changed = False
        for child, parent in enumerate(parents.tolist()):
            if int(parent) in bodies and child not in bodies:
                bodies.add(child)
                changed = True
    return bodies


def selector_body_ids(env, mask: MaskSelector) -> set[int]:
    names = model_body_names(env)
    if mask.kind == "drawer_part":
        fixture, slot = mask.value.split(":", 1)
        tokens = [f"{fixture}_cabinet_{slot}", f"{fixture}_{slot}"]
        roots = {idx for idx, name in enumerate(names) if any(token in name for token in tokens)}
    else:
        value = mask.value.lower()
        roots = {
            idx
            for idx, name in enumerate(names)
            if name.lower() == value
            or name.lower().startswith(value + "_")
            or value in name.lower()
        }
    return descendant_bodies(env, roots) if roots else set()


def render_body_mask(env, mask: MaskSelector, image_size: int = 320) -> np.ndarray | None:
    body_ids = selector_body_ids(env, mask)
    if not body_ids:
        return None
    seg = np.asarray(env.sim.render(camera_name="agentview", width=image_size, height=image_size, segmentation=True))
    if seg.ndim != 3 or seg.shape[-1] < 2:
        return None
    geom_body = np.asarray(env.sim.model.geom_bodyid, dtype=np.int32)
    geom_ids = np.flatnonzero(np.isin(geom_body, np.asarray(sorted(body_ids), dtype=np.int32)))
    if not len(geom_ids):
        return None
    if np.any(seg[..., 0] == 5):
        output = np.logical_and(seg[..., 0] == 5, np.isin(seg[..., 1], geom_ids)).astype(np.uint8)
    else:
        output = np.isin(seg[..., 1], geom_ids).astype(np.uint8)
    if mask.kind == "body_prefix" and re.fullmatch(r"flat_stove_\d+_button", mask.value):
        # LIBERO's stove mesh assigns a few disconnected burner-detail pixels
        # to the same visual geom as the rotary knob.  Retain only the largest
        # connected component so the review/evaluator mask is visually and
        # semantically knob-only.
        import cv2

        component_count, labels, stats, _centroids = cv2.connectedComponentsWithStats(
            output.astype(np.uint8), connectivity=8
        )
        if component_count > 1:
            largest = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
            output = (labels == largest).astype(np.uint8)
    # RGB observations are flipped vertically by the LIBERO wrapper/exporter,
    # but are not mirrored horizontally.  Apply the same vertical-only flip
    # to segmentation so overlays stay on the exact visible instance.
    output = np.ascontiguousarray(output[::-1, :])
    return output if output.any() else None


def parse_region_range(bddl_path: Path, full_name: str) -> tuple[float, float, float, float]:
    short = full_name
    for prefix in ("main_table_", "kitchen_table_", "living_room_table_", "study_table_", "floor_"):
        if short.startswith(prefix):
            short = short[len(prefix) :]
            break
    text = bddl_path.read_text(encoding="utf-8")
    match = re.search(
        rf"\({re.escape(short)}\s+\(:target\s+[^)]+\)\s+\(:ranges\s*\(\s*\(([^)]*)\)",
        text,
        flags=re.DOTALL,
    )
    if not match:
        raise ValueError(f"region not found: {full_name}")
    values = tuple(float(value) for value in match.group(1).split())
    if len(values) != 4:
        raise ValueError(values)
    return values  # type: ignore[return-value]


def world_to_image(env, world: np.ndarray, size: int) -> tuple[int, int] | None:
    sim = env.sim
    camera_id = sim.model.camera_name2id("agentview")
    camera_pos = np.asarray(sim.data.cam_xpos[camera_id], dtype=np.float64)
    camera_mat = np.asarray(sim.data.cam_xmat[camera_id], dtype=np.float64).reshape(3, 3)
    camera_frame = camera_mat.T @ (np.asarray(world, dtype=np.float64) - camera_pos)
    depth = -camera_frame[2]
    if depth <= 1e-8:
        return None
    focal = size / (2.0 * np.tan(np.deg2rad(float(sim.model.cam_fovy[camera_id])) / 2.0))
    u_value = focal * camera_frame[0] / depth + size / 2.0
    v_value = focal * camera_frame[1] / depth + size / 2.0
    return int(np.clip(u_value, 0, size - 1)), int(np.clip(size - 1 - v_value, 0, size - 1))


def render_region_mask(env, bddl_path: Path, full_name: str, image_size: int = 320) -> np.ndarray | None:
    import cv2

    ranges = parse_region_range(bddl_path, full_name)
    table_name = "table"
    if full_name.startswith("kitchen_table_"):
        table_name = "kitchen_table"
    elif full_name.startswith("living_room_table_"):
        table_name = "living_room_table"
    elif full_name.startswith("study_table_"):
        table_name = "study_table"
    elif full_name.startswith("floor_"):
        table_name = "floor"
    table_id = env.sim.model.body_name2id(table_name)
    table_pos = np.asarray(env.sim.data.body_xpos[table_id], dtype=np.float64)
    surface_z = float(table_pos[2] + 0.82)
    object_z: list[float] = []
    for name, body_id in getattr(env.env, "obj_body_id", {}).items():
        if str(name).startswith(("plate", "akita_black_bowl", "porcelain_mug")):
            object_z.append(float(env.sim.data.body_xpos[body_id][2]))
    if object_z:
        surface_z = min(object_z)
    x0, y0, x1, y1 = ranges
    corners = [
        np.array([table_pos[0] + x0, table_pos[1] + y0, surface_z]),
        np.array([table_pos[0] + x1, table_pos[1] + y0, surface_z]),
        np.array([table_pos[0] + x1, table_pos[1] + y1, surface_z]),
        np.array([table_pos[0] + x0, table_pos[1] + y1, surface_z]),
    ]
    points = [world_to_image(env, corner, image_size) for corner in corners]
    if any(point is None for point in points):
        return None
    poly = np.asarray(points, dtype=np.int32).reshape((-1, 1, 2))
    output = np.zeros((image_size, image_size), dtype=np.uint8)
    cv2.fillConvexPoly(output, poly, 1)
    return output if output.any() else None


def render_scene(OffScreenRenderEnv, bddl_path: Path, init_path: Path, masks: list[MaskSelector]) -> tuple[np.ndarray, dict[str, np.ndarray], dict[str, int]]:
    env = OffScreenRenderEnv(
        bddl_file_name=str(bddl_path),
        camera_heights=320,
        camera_widths=320,
        camera_names=["agentview"],
        render_gpu_device_id=int(os.environ.get("MUJOCO_EGL_DEVICE_ID", "6")),
    )
    try:
        env.reset()
        obs = env.set_init_state(np.asarray(load_init_array(init_path)[0]))
        if obs is None:
            obs, _, _, _ = env.step(DUMMY_ACTION)
        if env.check_success():
            raise RuntimeError(f"initial state already satisfies the task goal: {bddl_path}")
        image = np.flipud(np.asarray(obs["agentview_image"]))
        rendered_masks: dict[str, np.ndarray] = {}
        areas: dict[str, int] = {}
        for binding in masks:
            if binding.kind == "table_region":
                value = render_region_mask(env, bddl_path, binding.value)
            else:
                value = render_body_mask(env, binding)
            if value is None:
                raise RuntimeError(f"mask resolution failed: {binding.role}/{binding.kind}/{binding.value}")
            rendered_masks[binding.role] = value
            areas[binding.role] = int(value.sum())
        return image, rendered_masks, areas
    finally:
        env.close()


def overlay(
    image: np.ndarray,
    masks: dict[str, np.ndarray],
    bindings: list[MaskSelector] | None = None,
) -> Image.Image:
    output = Image.fromarray(image).convert("RGB")
    array = np.asarray(output).astype(np.float32)
    colors = {
        "manipulated_object": np.array([30, 200, 80], dtype=np.float32),
        "interaction_target": np.array([25, 190, 210], dtype=np.float32),
        "goal_target": np.array([255, 196, 20], dtype=np.float32),
    }
    explicit = {
        binding.role: {
            "green": np.array([30, 200, 80], dtype=np.float32),
            "cyan": np.array([25, 190, 210], dtype=np.float32),
            "yellow": np.array([255, 196, 20], dtype=np.float32),
        }[binding.color]
        for binding in (bindings or [])
    }
    for role, mask in masks.items():
        active = mask.astype(bool)
        color = explicit.get(
            role, colors.get(role, np.array([255, 80, 80], dtype=np.float32))
        )
        array[active] = 0.48 * array[active] + 0.52 * color
    return Image.fromarray(np.clip(array, 0, 255).astype(np.uint8))


def comparison_canvas(spec: Spec, source_img: np.ndarray, new_img: np.ndarray, masks: dict[str, np.ndarray]) -> Image.Image:
    width, panel = 1280, 560
    margin, gap = 48, 64
    header = 275
    canvas = Image.new("RGB", (width, header + panel + 50), "#f5f2eb")
    draw = ImageDraw.Draw(canvas)
    title_font = load_font(30, True)
    body_font = load_font(21)
    small_font = load_font(18)
    draw.text((margin, 20), f"{spec.task_id} | {spec.family}", fill="#171717", font=title_font)
    y_value = 64
    for prefix, value, font_value, color in (
        ("ORIGINAL: ", spec.source_instruction, body_font, "#24522f"),
        ("NEW: ", spec.language, body_font, "#164d82"),
    ):
        lines = fit_lines(draw, prefix + value, font_value, width - 2 * margin)
        for line in lines:
            draw.text((margin, y_value), line, fill=color, font=font_value)
            y_value += 28
    delta = "Changed: " + "; ".join(spec.varied)
    for line in fit_lines(draw, delta, small_font, width - 2 * margin):
        draw.text((margin, y_value + 3), line, fill="#4b4b4b", font=small_font)
        y_value += 24
    draw.text(
        (margin, header - 35),
        "Green = manipulated object   Cyan = articulated control   Yellow = exact destination",
        fill="#4c4c4c",
        font=small_font,
    )

    left_x = margin
    right_x = margin + panel + gap
    source_panel = Image.fromarray(source_img).resize((panel, panel), Image.Resampling.LANCZOS)
    new_panel = overlay(new_img, masks, spec.masks).resize(
        (panel, panel), Image.Resampling.LANCZOS
    )
    canvas.paste(source_panel, (left_x, header))
    canvas.paste(new_panel, (right_x, header))
    draw.rectangle((left_x, header, left_x + panel - 1, header + panel - 1), outline="#4f8d5e", width=5)
    draw.rectangle((right_x, header, right_x + panel - 1, header + panel - 1), outline="#367ab5", width=5)
    draw.rectangle((left_x, header, left_x + panel, header + 40), fill="#173d23")
    draw.rectangle((right_x, header, right_x + panel, header + 40), fill="#153e62")
    draw.text(
        (left_x + 14, header + 7),
        "Original LIBERO-40 scene + exact masks",
        fill="white",
        font=load_font(20, True),
    )
    draw.text((right_x + 14, header + 7), "Analogy scene + exact GT masks", fill="white", font=load_font(20, True))
    return canvas


def render_comparisons(specs: list[Spec], bundles: dict[str, Path], root: Path) -> dict[str, dict[str, int]]:
    base = import_scaffold_helpers()
    base.ensure_runtime_env()
    base.disable_interactive_pdb()
    patch_robosuite_segmentation_uint8_overflow()
    OffScreenRenderEnv = base.load_env_cls()
    png_root = root / "comparison_png"
    raw_root = png_root / "raw"
    raw_root.mkdir(parents=True)
    source_cache: dict[tuple[str, str], np.ndarray] = {}
    results: dict[str, dict[str, int]] = {}
    pair_paths: list[Path] = []
    total = len(specs)
    for index, spec in enumerate(specs, start=1):
        cache_key = (str(spec.source_bddl), str(spec.source_init))
        if cache_key not in source_cache:
            source_cache[cache_key] = original_masked_scene(spec.source_bddl)
        new_image, masks, areas = render_scene(
            OffScreenRenderEnv,
            bundles[spec.task_id] / "task.bddl",
            bundles[spec.task_id] / "task.pruned_init",
            spec.masks,
        )
        source_image = source_cache[cache_key]
        Image.fromarray(source_image).save(raw_root / f"{spec.task_id}__source.png")
        Image.fromarray(new_image).save(raw_root / f"{spec.task_id}__new.png")
        for role, value in masks.items():
            Image.fromarray((value * 255).astype(np.uint8)).save(raw_root / f"{spec.task_id}__mask_{role}.png")
        pair = comparison_canvas(spec, source_image, new_image, masks)
        pair_path = png_root / f"{spec.task_id}__{slugify(spec.language)}.png"
        pair.save(pair_path)
        pair_paths.append(pair_path)
        results[spec.task_id] = areas
        print(f"[render {index:03d}/{total}] {spec.task_id} masks={areas}", flush=True)

    thumb_w, thumb_h, columns = 320, 238, 4
    rows = (len(pair_paths) + columns - 1) // columns
    sheet = Image.new("RGB", (columns * thumb_w, rows * thumb_h), "#e9e5dc")
    for index, path in enumerate(pair_paths):
        image = Image.open(path).convert("RGB")
        image.thumbnail((thumb_w - 8, thumb_h - 8), Image.Resampling.LANCZOS)
        x_value = (index % columns) * thumb_w + (thumb_w - image.width) // 2
        y_value = (index // columns) * thumb_h + (thumb_h - image.height) // 2
        sheet.paste(image, (x_value, y_value))
    sheet.save(png_root / "ALL_ANALOGY_CANDIDATES_CONTACT_SHEET.png")
    return results


def normalized_bddl(path: Path) -> str:
    text = re.sub(r";[^\n]*", "", path.read_text(encoding="utf-8").lower())
    return re.sub(r"\s+", "", text)


def write_indexes(
    root: Path,
    specs: list[Spec],
    bundles: dict[str, Path],
    mask_areas: dict[str, dict[str, int]],
) -> None:
    family_counts: dict[str, int] = {}
    for spec in specs:
        family_counts[spec.family] = family_counts.get(spec.family, 0) + 1

    rows: list[dict[str, Any]] = []
    registry: list[str] = []
    action_plans: dict[str, list[dict[str, Any]]] = {}
    mask_registry: dict[str, Any] = {}
    for spec in specs:
        bundle = bundles[spec.task_id]
        rel = bundle.relative_to(root).as_posix()
        pair = next((root / "comparison_png").glob(f"{spec.task_id}__*.png"))
        rows.append(
            {
                "task_id": spec.task_id,
                "family": spec.family,
                "source_suite": spec.source_suite,
                "source_task_id": "" if spec.source_task_id is None else spec.source_task_id,
                "source_task": spec.source_bddl.stem,
                "original_instruction": spec.source_instruction,
                "new_instruction": spec.language,
                "goal_atom": spec.goal_atom,
                "physical_group": spec.physical_group,
                "evidence_notes": " | ".join(spec.notes),
                "init_states": len(load_init_array(bundle / "task.pruned_init")),
                "comparison_png": pair.relative_to(root).as_posix(),
                "bundle": rel,
            }
        )
        registry.append(f"{rel}/registry_entry.yaml")
        action_plans[spec.task_id] = spec.action_plan
        mask_registry[spec.task_id] = {
            "bindings": [vars(value) for value in spec.masks],
            "rendered_mask_areas_px_at_320": mask_areas[spec.task_id],
        }

    with (root / "TASK_INDEX.tsv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)
    dump_yaml(root / "registry.yaml", {"registry_entries": registry})
    dump_yaml(root / "action_plan_registry.yaml", {"action_plans": action_plans})
    # The RAIN evaluator resolves custom benchmark registries from this
    # conventional support directory.  Keep the human-facing root indexes and
    # emit evaluator-facing copies from the same in-memory data so they cannot
    # drift apart.
    support_root = root / "benchmark_support"
    support_root.mkdir(parents=True, exist_ok=True)
    dump_yaml(
        support_root / "benchmark_registry_candidates.yaml",
        {"registry_entries": registry},
    )
    dump_yaml(
        support_root / "action_plan_registry.yaml",
        {"action_plans": action_plans},
    )
    dump_yaml(
        root / "mask_registry.yaml",
        {
            "policy": "exact_instance_no_union",
            "region_masks_are_projected_from_each_current_task_bddl": True,
            "tasks": mask_registry,
        },
    )

    md = [
        "# LIBERO Analogy candidate index",
        "",
        f"- Candidate count: **{len(specs)}**",
        "- Task form: one semantic goal atom per task; no `and` composition",
        "- Evaluation status: task definitions and simulator/mask validation complete; policy inference not run",
        "- Rules: [ANALOGY_RULES.md](ANALOGY_RULES.md)",
        "- Overview image: [ALL_ANALOGY_CANDIDATES_CONTACT_SHEET.png](comparison_png/ALL_ANALOGY_CANDIDATES_CONTACT_SHEET.png)",
        "",
        "## Counts",
        "",
        "| Family | Count |",
        "|---|---:|",
    ]
    for family, count in family_counts.items():
        md.append(f"| `{family}` | {count} |")
    md.extend(
        [
            "",
            "## Tasks",
            "",
            "| ID | Family | Original LIBERO-40 instruction | New analogy instruction | Goal | Compare |",
            "|---|---|---|---|---|---|",
        ]
    )
    for row in rows:
        md.append(
            f"| `{row['task_id']}` | `{row['family']}` | {row['original_instruction']} | "
            f"{row['new_instruction']} | `{row['goal_atom']}` | [PNG]({row['comparison_png']}) |"
        )
    (root / "README.md").write_text("\n".join(md) + "\n", encoding="utf-8")


def rules_document() -> str:
    return textwrap.dedent(
        """\
        # LIBERO Analogy definition rules

        ## 1. Category meaning

        An Analogy task tests whether a **single skill/relation learned in the original LIBERO-40** is applied after changing one structural binding. The task is not a conjunction and is not obtained by taking a goal subset from a compound instruction.

        A candidate is accepted only when all of the following stay fixed:

        - the manipulated object identity;
        - the action predicate or final relation (`Open`, `Turnon`, `On`, or `In`);
        - the target fixture/receptacle type, except for a sibling part of the same drawer fixture;
        - one semantic goal atom.

        The changed variable must be one of:

        1. a second position already used as a target-interaction position in LIBERO-40;
        2. the exact instance binding among repeated same-type targets;
        3. a sibling articulated part (`top`, `middle`, `bottom`);
        4. the pose of a reference fixture, with every reference-relative goal region translated with it;
        5. a collision-free mirrored/adjacent receptacle slot on the same source table.

        ## 2. Single-task rule

        - Every BDDL has exactly one required goal atom.
        - Wording does not contain an action-level `and`.
        - A drawer-insertion target is initialized open in the sibling-slot family. This isolates insertion analogy from latent open+insert composition.
        - Source tasks that were compound may provide a learned primitive, but the new task itself remains atomic.

        ## 3. Novelty and deduplication

        A candidate is excluded if its complete physical initialization plus goal is an original LIBERO-40 task. Two candidates are distinct only if at least one of physical initialization, exact target instance/part, or canonical goal differs. Paraphrases and reversed wording do not create new tasks.

        Object substitution is deliberately outside this pool. Earlier DifferentTargetSameLayout/Object-Grounding candidates can be attached later as a separate analogy subfamily, but are not counted here.

        ## 4. Reachability and physical validity

        Continuous tabletop coordinates are not enumerated. The finite candidate lattice consists of:

        - original LIBERO-40 interaction positions;
        - left/middle/right target slots formed inside the source table envelope;
        - mirrored or adjacent fixture/receptacle slots on the same source surface.

        Every generated layout must pass all gates:

        1. BDDL parses and simulator reset succeeds;
        2. 50 stable non-success initial states are generated;
        3. critical objects do not fall or drift beyond the stability tolerance;
        4. task-critical objects/parts are visible in the agent camera;
        5. exact GT masks are non-empty.

        Thus “wherever” means every enumerated, reset-stable, visible slot in this benchmark definition—not the continuum of arbitrary coordinates.

        ## 5. GT-mask rules

        - **No instance union:** when three plates exist, only the instructed `plate_1`, `plate_2`, or `plate_3` is the placement mask.
        - **New instance lookup:** `plate_3` is resolved from the current simulator model by exact instance name; it must not fall back to a source episode JSON entry or to `plate_1/plate_2`.
        - **Drawer mask:** use the exact top/middle/bottom drawer body named in the instruction; never mask the whole cabinet or all drawer handles together.
        - **Reference-relative region:** for stove push, project `main_table_stove_front_region` from the current task BDDL after stove relocation. The old absolute source-region mask is forbidden.
        - **Placement target:** grasp/manipulation masks and placement masks are recorded separately in each task's `mask_bindings.yaml`.
        - Every comparison PNG overlays the masks resolved from the generated simulator state: green for the manipulated/interaction target and yellow for the exact destination.

        ## 6. Candidate families in this build

        | Family | Count | Rule |
        |---|---:|---|
        | Same object, seen target position | 10 | Each LIBERO-Object target moves to the other position used as an original target-grasp position. |
        | Exact target instance among three plates | 4 | All novel bindings for the two trained mugs after adding a middle plate. |
        | Sibling drawer slot | 4 | Black-bowl insertion transfers to the two missing sibling slots for white and wooden cabinets. |
        | Relocated articulated fixture | 2 | Open the same wooden-cabinet drawer after moving the cabinet to the opposite reachable side. |
        | Relocated stove/reference region | 4 | Turn on, push relative to, place on, or pick from the same stove at a donor pose. |
        | Relocated receptacle | 3 | Basket, desk caddy, and microwave move on their original source table. |
        | **Total** | **27** | Definitions only; later evaluation selects the final 20. |
        """
    )


def validate(root: Path, specs: list[Spec], bundles: dict[str, Path], state_count: int) -> None:
    ids = [spec.task_id for spec in specs]
    assert ids == [f"ANLG_{index:03d}" for index in range(1, 28)]
    signatures: set[str] = set()
    hashes: set[str] = set()
    for spec in specs:
        bundle = bundles[spec.task_id]
        metadata = load_yaml(bundle / "task_meta.yaml")
        signature = str(metadata["canonical_task_signature"])
        if signature in signatures:
            raise RuntimeError(f"duplicate canonical signature: {signature}")
        signatures.add(signature)
        digest = hashlib.sha256(normalized_bddl(bundle / "task.bddl").encode("utf-8")).hexdigest()
        if digest in hashes:
            raise RuntimeError(f"duplicate normalized BDDL: {spec.task_id}")
        hashes.add(digest)
        states = load_init_array(bundle / "task.pruned_init")
        if len(states) != state_count:
            raise RuntimeError(f"{spec.task_id}: {len(states)} init states")
        if len(spec.goal_atom.split(",")) > 2:
            raise RuntimeError(spec.goal_atom)
    dump_yaml(
        root / "VALIDATION.yaml",
        {
            "task_count": len(specs),
            "sequential_ids": True,
            "unique_canonical_signatures": len(signatures),
            "unique_normalized_bddls": len(hashes),
            "init_states_per_task": state_count,
            "policy_inference_run": False,
            "simulator_render_and_mask_validation": True,
        },
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--state-count", type=int, default=50)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.state_count < 1:
        raise ValueError(args.state_count)
    for path in (LIBERO_ROOT, POSITION_SWAP_ROOT, SCRIPT_ROOT):
        if not path.exists():
            raise FileNotFoundError(path)
    if OUTPUT_ROOT.exists() and not args.overwrite:
        raise FileExistsError(f"refusing to overwrite {OUTPUT_ROOT}")

    os.environ.setdefault("CUDA_VISIBLE_DEVICES", "6,7")
    os.environ.setdefault("MUJOCO_EGL_DEVICE_ID", "6")
    os.environ.setdefault("MUJOCO_GL", "egl")
    os.environ.setdefault("PYOPENGL_PLATFORM", "egl")

    specs = build_specs()
    stage_parent = Path(tempfile.mkdtemp(prefix=".LiberoAnalogy_", dir=HERE))
    stage = stage_parent / OUTPUT_ROOT.name
    stage.mkdir()
    try:
        bundles: dict[str, Path] = {}
        bddl_by_id: dict[str, str] = {}
        for spec in specs:
            if spec.copied_from is not None:
                text = spec.copied_from.joinpath("task.bddl").read_text(encoding="utf-8")
                text = replace_language(text, spec.language)
                text = replace_interest(text, spec.objects_of_interest)
                text = replace_goal(text, spec.goal_bddl)
            else:
                text = base_transform(spec, spec.source_bddl.read_text(encoding="utf-8"))
            bddl_by_id[spec.task_id] = text
            bundles[spec.task_id] = write_task_bundle(stage, spec, text)

        copy_or_generate_init(specs, bundles, bddl_by_id, args.state_count)
        mask_areas = render_comparisons(specs, bundles, stage)
        (stage / "ANALOGY_RULES.md").write_text(rules_document(), encoding="utf-8")
        write_indexes(stage, specs, bundles, mask_areas)
        validate(stage, specs, bundles, args.state_count)

        if OUTPUT_ROOT.exists():
            backup = HERE / f".{OUTPUT_ROOT.name}.old"
            if backup.exists():
                shutil.rmtree(backup)
            OUTPUT_ROOT.rename(backup)
            stage.rename(OUTPUT_ROOT)
            shutil.rmtree(backup)
        else:
            stage.rename(OUTPUT_ROOT)
        print(f"Built {len(specs)} tasks at {OUTPUT_ROOT}", flush=True)
    finally:
        if stage_parent.exists():
            shutil.rmtree(stage_parent)


if __name__ == "__main__":
    main()
