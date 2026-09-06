#!/usr/bin/env python3
"""Build the six WTRAY reachability revisions without touching WTRAY.

The wooden tray is translated 6 cm toward robot-right in every task.  In the
heterogeneous scene only, the black bowl is moved to a slightly more central,
reachable pickup pose.  Plate poses and the ramekin / white-bowl poses remain
exactly as in WTRAY_001..006.  Five fresh simulator states are generated for
every revision; no policy inference is performed here.
"""

from __future__ import annotations

import csv
import dataclasses
import hashlib
import json
from pathlib import Path

import numpy as np
import yaml

import build_libero_adapt_cross_suite as cross
import build_libero_analogy as base
import build_libero_diverse_adapt as pipeline
import build_libero_wooden_tray_object_choices as predecessor
import novel_scene_common as canonical


ROOT = Path(__file__).resolve().parent
SOURCE_BENCHMARK = ROOT / "LiberoWoodenTrayObjectChoices"
OUTPUT = ROOT / "LiberoWoodenTrayObjectChoicesReachable"
ID_PREFIX = "WTRAYR"
TARGET_REGION = predecessor.TARGET_REGION

OLD_TRAY_CENTER_XY = (0.10, 0.00)
NEW_TRAY_CENTER_XY = (0.10, -0.06)
OLD_BLACK_BOWL_CENTER_XY = (-0.13, -0.23)
NEW_BLACK_BOWL_CENTER_XY = (-0.16, -0.18)
UNCHANGED_CHOICE_CENTERS_XY = dict(predecessor.CHOICE_CENTERS_XY)
FRESH_SEED_BASE = 1_737_000

PLATE_FAMILY = "F1_three_plate_choice"
HETEROGENEOUS_FAMILY = "F2_heterogeneous_dishware_choice"
BLACK_BOWL_ID = "akita_black_bowl_1"


class InitWorkerReference:
    """Hash the exact revision builder and every initialization dependency."""

    def __str__(self) -> str:
        return str(ROOT / "run_wooden_tray_object_choices_init_worker.py")

    def read_text(self) -> str:
        paths = [
            ROOT / "build_libero_wooden_tray_object_choices_reachable.py",
            ROOT / "build_libero_wooden_tray_object_choices.py",
            ROOT / "run_wooden_tray_object_choices_init_worker.py",
            ROOT / "run_diverse_adapt_init_worker.py",
            ROOT / "run_adapt_init_worker.py",
            ROOT / "novel_feedback_fixture_geometry.py",
            ROOT / "novel_scene_physics.py",
            ROOT / "novel_scene_mask_geometry.py",
            ROOT / "novel_scene_init_support.py",
        ]
        return "\n".join(
            f"{path}\n{path.read_text(encoding='utf-8')}" for path in paths
        )


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(
            stream, fieldnames=fields, delimiter="\t", extrasaction="ignore"
        )
        writer.writeheader()
        writer.writerows(rows)


def source_snapshot() -> dict[str, str]:
    if not SOURCE_BENCHMARK.is_dir():
        raise FileNotFoundError(SOURCE_BENCHMARK)
    return {
        str(path.relative_to(SOURCE_BENCHMARK)): sha256(path)
        for path in sorted(SOURCE_BENCHMARK.rglob("*"))
        if path.is_file()
    }


def _rectangle(center: tuple[float, float], half: float = 0.003) -> str:
    x_value, y_value = center
    return (
        f"({x_value-half:.6f} {y_value-half:.6f} "
        f"{x_value+half:.6f} {y_value+half:.6f})"
    )


def _choice_center(
    family: str, object_id: str, position: str
) -> tuple[float, float]:
    if family == HETEROGENEOUS_FAMILY and object_id == BLACK_BOWL_ID:
        return NEW_BLACK_BOWL_CENTER_XY
    return UNCHANGED_CHOICE_CENTERS_XY[position]


def scene_text(
    choices: list[tuple[str, str, str, str]], family: str
) -> str:
    """Return the controlled revised scene for one three-choice family."""

    by_type: dict[str, list[str]] = {}
    for object_id, object_type, _, _ in choices:
        by_type.setdefault(object_type, []).append(object_id)
    object_lines = [
        f"    {' '.join(object_ids)} - {object_type}"
        for object_type, object_ids in by_type.items()
    ]
    init_lines = [
        f"    (On {object_id} living_room_table_choice_{position}_init_region)"
        for object_id, _, _, position in choices
    ]
    regions = [
        "\n".join(
            [
                "      (wooden_tray_1_init_region",
                "          (:target living_room_table)",
                f"          (:ranges ({_rectangle(NEW_TRAY_CENTER_XY, 0.001)}))",
                "          (:yaw_rotation ((0.0 0.0)))",
                "      )",
            ]
        )
    ]
    by_position = {item[3]: item[0] for item in choices}
    for position in ("left", "middle", "right"):
        center = _choice_center(family, by_position[position], position)
        regions.append(
            "\n".join(
                [
                    f"      (choice_{position}_init_region",
                    "          (:target living_room_table)",
                    f"          (:ranges ({_rectangle(center)}))",
                    "          (:yaw_rotation ((0.0 0.0)))",
                    "      )",
                ]
            )
        )
    regions.append(
        "\n".join(
            [
                "      (contain_region",
                "          (:target wooden_tray_1)",
                "      )",
            ]
        )
    )
    return "\n".join(
        [
            f"; Reachable wooden-tray revision: {family}.",
            "(define (problem libero_living_room_tabletop_manipulation)",
            "  (:domain robosuite)",
            "  (:language PLACEHOLDER.)",
            "  (:regions",
            *regions,
            "  )",
            "",
            "  (:fixtures",
            "    living_room_table - living_room_table",
            "  )",
            "",
            "  (:objects",
            "    wooden_tray_1 - wooden_tray",
            *object_lines,
            "  )",
            "",
            "  (:obj_of_interest",
            "    wooden_tray_1_contain_region",
            "  )",
            "",
            "  (:init",
            "    (On wooden_tray_1 living_room_table_wooden_tray_1_init_region)",
            *init_lines,
            "  )",
            "",
            "  (:goal",
            "    (And (In " + choices[0][0] + " " + TARGET_REGION + "))",
            "  )",
            "",
            ")",
            "",
        ]
    )


def candidates() -> list[cross.Candidate]:
    """Retain six tasks and replace only the controlled scene geometry."""

    values: list[cross.Candidate] = []
    for ordinal, candidate in enumerate(predecessor.candidates(), 1):
        family = candidate.spec.family
        choices = (
            predecessor.PLATE_CHOICES
            if family == PLATE_FAMILY
            else predecessor.HETEROGENEOUS_CHOICES
        )
        template = scene_text(choices, family)
        predecessor_id = f"WTRAY_{ordinal:03d}"
        varied = list(candidate.spec.varied) + [
            "translate wooden_tray_1 center from (0.10,0.00) to (0.10,-0.06)"
        ]
        if family == HETEROGENEOUS_FAMILY:
            varied.append(
                "translate only akita_black_bowl_1 from (-0.13,-0.23) to (-0.16,-0.18)"
            )
        fixed = [
            "task language, selected object, exact single In goal, and action plan",
            "unscaled wooden_tray asset, yaw, collision geometry, and native contain_region",
            "all three plate centers" if family == PLATE_FAMILY else "ramekin and white-bowl centers",
            "all three choices visible and initially outside the tray",
        ]
        notes = [
            "Direct controlled revision of " + predecessor_id + ".",
            "Tray center changes by (dx,dy)=(0.00,-0.06) m to robot-right.",
            (
                "All pickup centers are unchanged."
                if family == PLATE_FAMILY
                else "Only the black-bowl pickup center changes by (dx,dy)=(-0.03,+0.05) m; ramekin and white bowl are unchanged."
            ),
            "The native tray site and exact two-mask policy are unchanged.",
            "Strict success remains native In plus full collision containment, positive tray contact, release, and a five-control-step hold.",
        ]
        spec = dataclasses.replace(
            candidate.spec,
            transform=lambda _text, template=template: template,
            varied=varied,
            held_fixed=fixed,
            physical_group=candidate.spec.physical_group + "_reachable_pose_revision",
            notes=notes,
        )
        evidence = list(candidate.evidence) + [
            {
                "task_id": predecessor_id,
                "role": "DIRECT PREDECESSOR",
                "reason": "same task with the pre-revision tray and pickup geometry",
            }
        ]
        values.append(
            dataclasses.replace(candidate, spec=spec, evidence=evidence)
        )
    return values


def _predecessor_id(candidate: cross.Candidate) -> str:
    ordered = [item.spec.goal_atom for item in candidates()]
    return f"WTRAY_{ordered.index(candidate.spec.goal_atom) + 1:03d}"


def patch_meta(bundle: Path, candidate: cross.Candidate) -> None:
    predecessor.patch_meta(bundle, candidate)
    meta = base.load_yaml(bundle / "task_meta.yaml")
    source_id = _predecessor_id(candidate)
    meta.update(
        adapt_scope="wooden_tray_reachable_pose_revision",
        predecessor_task_id=source_id,
        controlled_revision=True,
        old_tray_center_xy_m=list(OLD_TRAY_CENTER_XY),
        new_tray_center_xy_m=list(NEW_TRAY_CENTER_XY),
        tray_translation_delta_xy_m=[0.0, -0.06],
        black_bowl_shift_applies=(candidate.spec.family == HETEROGENEOUS_FAMILY),
        old_black_bowl_center_xy_m=list(OLD_BLACK_BOWL_CENTER_XY),
        new_black_bowl_center_xy_m=list(NEW_BLACK_BOWL_CENTER_XY),
        black_bowl_translation_delta_xy_m=[-0.03, 0.05],
        plate_centers_unchanged=True,
        ramekin_center_unchanged=True,
        white_bowl_center_unchanged=True,
        source_state_reuse_allowed=False,
        fresh_state_seed_base=FRESH_SEED_BASE,
        definition_status="defined_pending_five_state_init_validation",
        policy_inference_run=False,
        github_upload_performed=False,
    )
    base.dump_yaml(bundle / "task_meta.yaml", meta)


def comparison_canvas(
    candidate: cross.Candidate,
    stage: Path,
    catalog: dict[str, dict[str, str]],
    evaluated_label: str = "REACHABLE WOODEN-TRAY REVISION",
):
    """Create the normal provenance canvas before direct old/new replacement."""

    return predecessor.comparison_canvas(
        candidate, stage, catalog, evaluated_label=evaluated_label
    )


def write_revision_comparisons() -> None:
    from PIL import Image, ImageDraw, ImageFont

    directory = OUTPUT / "comparison_png"
    directory.mkdir(parents=True, exist_ok=True)
    for ordinal in range(1, 7):
        old_id = f"WTRAY_{ordinal:03d}"
        new_id = f"WTRAYR_{ordinal:03d}"
        old_path = (
            SOURCE_BENCHMARK / "comparison_png" / "raw" / f"{old_id}__new.png"
        )
        new_path = directory / "raw" / f"{new_id}__new.png"
        if not old_path.is_file() or not new_path.is_file():
            raise FileNotFoundError(f"missing old/new scene render for {new_id}")
        old = Image.open(old_path).convert("RGB")
        new = Image.open(new_path).convert("RGB")
        side = min(old.height, new.height)
        old.thumbnail((side, side))
        new.thumbnail((side, side))
        header = 64
        canvas = Image.new("RGB", (old.width + new.width, side + header), "white")
        canvas.paste(old, (0, header))
        canvas.paste(new, (old.width, header))
        draw = ImageDraw.Draw(canvas)
        font = ImageFont.load_default()
        draw.text(
            (8, 7),
            f"{old_id}: tray (0.10, 0.00)",
            fill="black",
            font=font,
        )
        draw.text(
            (old.width + 8, 7),
            f"{new_id}: tray (0.10, -0.06)",
            fill="black",
            font=font,
        )
        detail = (
            "Plate poses unchanged."
            if ordinal <= 3
            else "Black bowl: (-0.13,-0.23) -> (-0.16,-0.18); ramekin/white bowl unchanged."
        )
        draw.text(
            (8, 31),
            "Pure robot-right tray shift (0,-0.06) m. " + detail,
            fill="black",
            font=font,
        )
        canvas.save(directory / f"{new_id}__comparison.png", optimize=True)


def validate_and_document(before: dict[str, str]) -> None:
    after = source_snapshot()
    if after != before:
        changed = sorted(set(before) | set(after))
        changed = [key for key in changed if before.get(key) != after.get(key)]
        raise RuntimeError(f"predecessor WTRAY benchmark changed: {changed[:10]}")
    rows = read_tsv(OUTPUT / "TASK_INDEX.tsv")
    expected = [f"WTRAYR_{index:03d}" for index in range(1, 7)]
    if [row["task_id"] for row in rows] != expected:
        raise RuntimeError(f"complete ordered revision inventory required: {expected}")
    if (OUTPUT / "evaluation_5ep").exists():
        raise RuntimeError("builder must not create policy-evaluation results")

    required_tray_range = _rectangle(NEW_TRAY_CENTER_XY, 0.001)
    unchanged_ranges = {
        "middle": _rectangle(UNCHANGED_CHOICE_CENTERS_XY["middle"]),
        "right": _rectangle(UNCHANGED_CHOICE_CENTERS_XY["right"]),
    }
    validations = []
    for ordinal, row in enumerate(rows, 1):
        task_id = row["task_id"]
        bundle = OUTPUT / row["bundle"]
        bddl = (bundle / "task.bddl").read_text(encoding="utf-8")
        meta = base.load_yaml(bundle / "task_meta.yaml")
        rules = base.load_yaml(bundle / "eval_rules.yaml")
        masks = base.load_yaml(bundle / "mask_bindings.yaml")
        init_report = json.loads(
            (bundle / "INIT_VALIDATION.json").read_text(encoding="utf-8")
        )
        states = np.asarray(base.load_init_array(bundle / "task.pruned_init"))
        old_row = read_tsv(SOURCE_BENCHMARK / "TASK_INDEX.tsv")[ordinal - 1]
        old_bundle = SOURCE_BENCHMARK / old_row["bundle"]
        atoms = canonical.goal_atoms(canonical.sections(bddl))
        if (
            len(atoms) != 1
            or atoms[0][0] != "in"
            or atoms[0][2] != TARGET_REGION
            or bddl.count("(contain_region") != 1
            or "(:target wooden_tray_1)" not in bddl
            or required_tray_range not in bddl
            or "feedback_contain" in bddl
        ):
            raise RuntimeError(f"{task_id}: native one-goal tray definition differs")
        left_expected = (
            _rectangle(NEW_BLACK_BOWL_CENTER_XY)
            if ordinal >= 4
            else _rectangle(UNCHANGED_CHOICE_CENTERS_XY["left"])
        )
        if (
            left_expected not in bddl
            or unchanged_ranges["middle"] not in bddl
            or unchanged_ranges["right"] not in bddl
        ):
            raise RuntimeError(f"{task_id}: controlled choice coordinates differ")
        object_id = atoms[0][1]
        selectors = {
            (binding.get("role"), binding.get("kind"), binding.get("value"))
            for binding in list(masks.get("bindings") or [])
        }
        expected_selectors = {
            ("manipulated_object", "body_prefix", object_id + "_main"),
            ("goal_target", "table_region", TARGET_REGION),
        }
        if (
            masks.get("policy") != "exact_instance_no_union"
            or len(masks.get("bindings") or []) != 2
            or selectors != expected_selectors
            or any(
                binding.get("exact_instance") is not True
                for binding in masks.get("bindings") or []
            )
        ):
            raise RuntimeError(f"{task_id}: exact two-mask contract differs")
        if (
            rules.get("required_goal_atoms") != meta.get("canonical_goal_atoms")
            or rules.get("custom_eval_needed") is not True
            or rules.get("tray_completion_mode")
            != "full_containment_released_supported"
            or rules.get("support_hold_control_steps") != 5
            or rules.get("full_collision_containment_required") is not True
            or rules.get("positive_force_tray_contact_required") is not True
            or rules.get("no_gripper_contact_required") is not True
            or rules.get("target_support_site") != TARGET_REGION
        ):
            raise RuntimeError(f"{task_id}: strict physical rule differs")
        selected_indices = list(init_report.get("selected_indices") or [])
        selected_rows = {
            int(item["pool_index"]): item for item in init_report.get("rows") or []
        }
        if (
            states.shape[0] != 5
            or len({state.tobytes() for state in states}) != 5
            or len(selected_indices) != 5
            or not init_report.get("fresh_state_generation")
            or not init_report.get("all_initial_goals_checked_false")
            or not init_report.get("all_three_choice_masks_checked")
            or not init_report.get("all_three_choices_initially_outside_tray")
            or any(
                int(selected_rows[index]["mask_areas"].get("goal_target", 0)) <= 0
                or int(selected_rows[index]["mask_areas"].get("manipulated_object", 0)) <= 0
                for index in selected_indices
            )
            or sha256(bundle / "task.pruned_init")
            == sha256(old_bundle / "task.pruned_init")
        ):
            raise RuntimeError(f"{task_id}: fresh five-state audit differs")
        visibility = list(init_report.get("selected_state_choice_visibility") or [])
        if len(visibility) != 5 or any(
            len(item.get("choice_mask_areas") or {}) != 3
            or min(int(value) for value in item["choice_mask_areas"].values()) <= 0
            or not all(item.get("all_choice_objects_outside_tray", {}).values())
            for item in visibility
        ):
            raise RuntimeError(f"{task_id}: all-choice visibility audit differs")
        comparison = OUTPUT / row["comparison_png"]
        if not comparison.is_file() or comparison.stat().st_size <= 0:
            raise RuntimeError(f"{task_id}: old/new comparison is missing")
        meta["definition_status"] = "defined_and_five_state_simulator_validated"
        meta["fresh_initial_state_sha256"] = sha256(bundle / "task.pruned_init")
        base.dump_yaml(bundle / "task_meta.yaml", meta)
        validations.append(
            {
                "task_id": task_id,
                "predecessor_task_id": f"WTRAY_{ordinal:03d}",
                "bundle": row["bundle"],
                "task_bddl_sha256": sha256(bundle / "task.bddl"),
                "task_pruned_init_sha256": sha256(bundle / "task.pruned_init"),
                "comparison_png_sha256": sha256(comparison),
                "states": 5,
                "initial_goal_false": True,
                "exact_masks_visible": True,
            }
        )

    snapshot_rows = [
        {"relative_path": key, "sha256": value}
        for key, value in sorted(before.items())
    ]
    write_tsv(
        OUTPUT / "SOURCE_WTRAY_SNAPSHOT_SHA256.tsv",
        snapshot_rows,
        ["relative_path", "sha256"],
    )
    provenance_rows = []
    for ordinal, row in enumerate(rows, 1):
        provenance_rows.append(
            {
                "task_id": row["task_id"],
                "predecessor_task_id": f"WTRAY_{ordinal:03d}",
                "instruction": row["new_instruction"],
                "tray_old_xy_m": "0.10,0.00",
                "tray_new_xy_m": "0.10,-0.06",
                "black_bowl_old_xy_m": "-0.13,-0.23" if ordinal >= 4 else "unchanged/not-applicable",
                "black_bowl_new_xy_m": "-0.16,-0.18" if ordinal >= 4 else "unchanged/not-applicable",
                "other_choice_poses": "unchanged",
            }
        )
    write_tsv(
        OUTPUT / "REVISION_PROVENANCE.tsv",
        provenance_rows,
        list(provenance_rows[0]),
    )

    lines = [
        "# Reachable wooden-tray object-choice revisions",
        "",
        "Six controlled revisions preserve WTRAY_001..006 and their evaluation results.",
        "",
        "- `wooden_tray_1`: `(0.10,0.00)` → `(0.10,-0.06)`, a pure 6 cm robot-right translation in all tasks.",
        "- Heterogeneous family only: `akita_black_bowl_1`: `(-0.13,-0.23)` → `(-0.16,-0.18)`.",
        "- Plate centers, ramekin center, white-bowl center, object identities, language, action plans, goals, tray yaw, native site, and asset geometry are unchanged.",
        "- Each task has five freshly generated, distinct, settled, visible, initially goal-false states on physical GPU 6 or 7.",
        "- Exact masks are the selected object instance and the current native tray site only; stored/union masks are forbidden.",
        "- Evaluation must retain WTRAY's strict physical success rule. This builder performs no policy inference.",
        "",
        "| Revision | Predecessor | Instruction | Comparison |",
        "|---|---|---|---|",
    ]
    for ordinal, row in enumerate(rows, 1):
        lines.append(
            f"| `{row['task_id']}` | `WTRAY_{ordinal:03d}` | {row['new_instruction']} | [old/new PNG]({row['comparison_png']}) |"
        )
    (OUTPUT / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (OUTPUT / "DIVERSE_ADAPT_RULES.md").write_text(
        "\n".join(lines[:12]) + "\n", encoding="utf-8"
    )

    validation_path = OUTPUT / "BUILD_VALIDATION.json"
    validation = json.loads(validation_path.read_text(encoding="utf-8"))
    validation.update(
        revision_of="LiberoWoodenTrayObjectChoices/WTRAY_001..006",
        requested_task_count=6,
        all_requested_tasks_survived=True,
        final_task_ids=expected,
        build_physical_gpus=[6, 7],
        states_per_task=5,
        fresh_seed_base=FRESH_SEED_BASE,
        source_state_reuse_allowed=False,
        reuse_valid_cache=False,
        reuse_identical_physics_pools=False,
        old_tray_center_xy=list(OLD_TRAY_CENTER_XY),
        new_tray_center_xy=list(NEW_TRAY_CENTER_XY),
        tray_translation_delta_xy=[0.0, -0.06],
        old_black_bowl_center_xy=list(OLD_BLACK_BOWL_CENTER_XY),
        new_black_bowl_center_xy=list(NEW_BLACK_BOWL_CENTER_XY),
        black_bowl_translation_delta_xy=[-0.03, 0.05],
        all_plate_centers_unchanged=True,
        ramekin_and_white_bowl_centers_unchanged=True,
        native_wooden_tray_contain_region=True,
        exact_instance_no_union_masks=True,
        all_initial_goals_checked_false=True,
        all_three_choice_masks_checked=True,
        all_three_choices_initially_outside_tray=True,
        strict_success_protocol_unchanged=True,
        tray_completion_mode="full_containment_released_supported",
        support_hold_control_steps=5,
        predecessor_file_count=len(before),
        predecessor_snapshot_unchanged=True,
        task_validations=validations,
        policy_inference_run=False,
        github_upload_performed=False,
    )
    validation_path.write_text(
        json.dumps(validation, indent=2) + "\n", encoding="utf-8"
    )

    artifact_rows = [
        {
            "relative_path": str(path.relative_to(OUTPUT)),
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        }
        for path in sorted(OUTPUT.rglob("*"))
        if path.is_file() and path.name != "REVISION_ARTIFACT_SHA256.tsv"
    ]
    write_tsv(
        OUTPUT / "REVISION_ARTIFACT_SHA256.tsv",
        artifact_rows,
        ["relative_path", "bytes", "sha256"],
    )


def main() -> None:
    from novel_feedback_gpu_config import rebind_function

    if OUTPUT.exists():
        raise RuntimeError(f"refusing to overwrite existing revision: {OUTPUT}")
    before = source_snapshot()
    pipeline.main = rebind_function(
        pipeline.main,
        [
            ("gpu=(2,3)[order%2]", "gpu=(6,7)[order%2]"),
            (
                "str(1210000+order*1000)",
                f"str({FRESH_SEED_BASE}+order*1000)",
            ),
        ],
    )
    pipeline.DEFAULT_ROOT = OUTPUT
    pipeline.ID_PREFIX = ID_PREFIX
    pipeline.TITLE = "Reachable wooden-tray three-object choice revisions"
    pipeline.COMPARISON_LABEL = "REACHABLE WOODEN-TRAY REVISION"
    pipeline.INIT_WORKER = InitWorkerReference()
    pipeline.candidate_list = candidates
    pipeline.patch_meta = patch_meta
    pipeline.adapt.semantic_signature = canonical.physical_signature
    pipeline.adapt.original_signatures = lambda: set()
    cross.comparison_canvas = comparison_canvas
    pipeline.main()
    if not (OUTPUT / "TASK_INDEX.tsv").is_file():
        raise RuntimeError("revision build ended without TASK_INDEX.tsv")
    write_revision_comparisons()
    validate_and_document(before)
    print(f"Built and validated WTRAYR_001..006: {OUTPUT}")


if __name__ == "__main__":
    main()
