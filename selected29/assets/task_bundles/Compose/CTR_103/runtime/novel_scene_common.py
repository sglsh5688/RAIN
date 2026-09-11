"""Build new LIBERO furniture compositions and canonical physical signatures.

No simulator creation or task writing occurs here. Scene transforms retain only
the official workspace/robot frame; every object, fixture, region and initial
predicate is explicitly replaced. The design ID is provenance, not goal text.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
import re
from collections import defaultdict
from typing import Callable


def parse_bddl(text: str) -> list:
    tokens = re.findall(r"\(|\)|[^\s()]+", re.sub(r";[^\n]*", "", text))
    stack, result = [], None
    for token in tokens:
        if token == "(":
            value = []
            if stack:
                stack[-1].append(value)
            stack.append(value)
        elif token == ")":
            if not stack:
                raise ValueError("unbalanced BDDL")
            result = stack.pop()
        else:
            if not stack:
                raise ValueError("BDDL token outside expression")
            stack[-1].append(token.casefold())
    if stack or not isinstance(result, list) or not result or result[0] != "define":
        raise ValueError("invalid BDDL definition")
    return result


def sections(text: str) -> dict:
    return {value[0]: value[1:] for value in parse_bddl(text)[1:] if isinstance(value, list)}


def typed_declarations(tokens: list) -> dict[str, str]:
    result, pending, index = {}, [], 0
    while index < len(tokens):
        if tokens[index] == "-":
            if not pending or index + 1 >= len(tokens):
                raise ValueError("malformed typed declaration")
            result.update({name: tokens[index + 1] for name in pending})
            pending = []
            index += 2
        else:
            pending.append(tokens[index])
            index += 1
    result.update({name: "object" for name in pending})
    return result


def goal_atoms(data: dict) -> list[list[str]]:
    goal = data.get(":goal", [])
    if len(goal) == 1 and isinstance(goal[0], list) and goal[0] and goal[0][0] == "and":
        return goal[0][1:]
    return goal


def scene_transform(
    scene_id: str, *, fixtures: dict[str, str], objects: dict[str, str],
    placements: dict[str, tuple[float, float, float]],
    sites: list[tuple[str, str]] = (),
    extra_regions: list[tuple[str, str, tuple[float, float, float, float], float | None]] = (),
    initial: list[str] = (), jitter: float = .008,
) -> Callable[[str], str]:
    """Return a full reconstruction transform compatible with mk_candidate.

    ``scene_id`` is an arbitrary provenance key. Coordinates use the source
    workspace's local BDDL frame. ``sites`` declare existing named XML sites;
    they do not invent geometry. A supplied On/In initial predicate replaces an
    object's tabletop start. Movable class rotations override sampler yaw in
    installed LIBERO; yaw is dependable for fixtures only. Tabletop placement
    ranges use >=.035 m half-width because its sampler applies boundary checks.
    """
    entities = {**fixtures, **objects}
    if len(entities) != len(fixtures) + len(objects):
        raise ValueError("an instance cannot be both fixture and movable object")
    if set(placements) - set(entities):
        raise ValueError("placement references undeclared entity")

    def transform(source_text: str) -> str:
        original = sections(source_text)
        source_fixtures = typed_declarations(original[":fixtures"])
        workspaces = [(name, kind) for name, kind in source_fixtures.items() if "table" in kind or kind == "floor"]
        if len(workspaces) != 1:
            raise ValueError(f"expected one source workspace: {workspaces}")
        workspace, workspace_type = workspaces[0]
        if workspace in entities:
            raise ValueError("workspace is supplied automatically")
        generated_regions, generated_init = [], []

        def region(name, target, bounds=None, yaw=None):
            lines = [f"      ({name}", f"          (:target {target})"]
            if bounds is not None:
                lines.extend(["          (:ranges (", "              (" + " ".join(f"{v:.8f}" for v in bounds) + ")", "            )", "          )"])
            if yaw is not None:
                lines.extend(["          (:yaw_rotation (", f"              ({yaw:.12f} {yaw:.12f})", "            )", "          )"])
            lines.append("      )")
            generated_regions.append("\n".join(lines))

        supported = set()
        for expression in initial:
            match = re.fullmatch(r"\((?:On|In)\s+(\S+)\s+(\S+)\)", expression, re.IGNORECASE)
            if match:
                supported.add(match[1])
        for instance in entities:
            if instance in supported:
                continue
            if instance not in placements:
                raise ValueError(f"{scene_id}: no explicit start for {instance}")
            x, y, yaw = placements[instance]
            # Fixed-body model poses are not serialized in init qpos arrays;
            # reconstruct their identical xy/yaw for initialization/evaluation.
            # MuJoCo region sites need positive dimensions. The novel fixture
            # sampler snaps this tiny rectangle to its exact declared center.
            halfwidth = .0001 if instance in fixtures else (max(jitter, .035) if workspace_type == "table" else jitter)
            name = f"{instance}_init_region"
            region(name, workspace, (x-halfwidth, y-halfwidth, x+halfwidth, y+halfwidth), yaw)
            generated_init.append(f"(On {instance} {workspace}_{name})")
        for parent, suffix in sites:
            if parent not in entities:
                raise ValueError(f"{scene_id}: site parent not declared: {parent}")
            region(suffix, parent)
        for name, target, bounds, yaw in extra_regions:
            if target not in entities and target != workspace:
                raise ValueError(f"{scene_id}: extra-region target not declared: {target}")
            region(name, target, bounds, yaw)
        generated_init.extend(initial)
        all_fixtures = {workspace: workspace_type, **fixtures}
        fixture_lines = "\n".join(f"    {name} - {kind}" for name, kind in all_fixtures.items())
        object_lines = "\n".join(f"    {name} - {kind}" for name, kind in objects.items())
        init_lines = "\n".join(f"    {expression}" for expression in generated_init)
        problem = original["problem"][0]
        return (
            f"; New furniture composition: {scene_id}. Only workspace/robot frame retained.\n"
            f"(define (problem {problem})\n  (:domain robosuite)\n  (:language novel scene placeholder)\n"
            "    (:regions\n" + "\n".join(generated_regions) + "\n    )\n\n"
            f"  (:fixtures\n{fixture_lines}\n  )\n\n"
            f"  (:objects\n{object_lines}\n  )\n\n"
            "  (:obj_of_interest\n  )\n\n"
            f"  (:init\n{init_lines}\n  )\n\n"
            "  (:goal\n    (And)\n  )\n\n)\n"
        )
    return transform


def canonical_payload(text: str, include_goal: bool = True) -> dict:
    """Canonicalize physics/goal, ignoring language, comments and interest.

    Instance IDs are canonicalized over all permutations within an asset type.
    Sampled-region names are replaced by physical target/bounds/yaw; XML site
    suffixes remain meaningful. Declaration/region/predicate ordering and float
    formatting are normalized. This does not claim semantic equivalence of
    geometrically different regions, reflected scenes, or predicate rewrites.
    """
    data = sections(text)
    fixture_map = typed_declarations(data.get(":fixtures", []))
    object_map = typed_declarations(data.get(":objects", []))
    groups = defaultdict(list)
    for role, mapping in (("fixture", fixture_map), ("object", object_map)):
        for name, kind in mapping.items():
            groups[(role, kind)].append(name)
    options = []
    for (role, kind), names in sorted(groups.items()):
        labels = [f"{role}:{kind}:{index}" for index in range(len(names))]
        options.append([dict(zip(order, labels)) for order in itertools.permutations(sorted(names))])
    possibilities = math.prod(map(len, options))
    if possibilities > 100_000:
        raise ValueError(f"too many repeated-instance canonicalizations: {possibilities}")
    best_key, best = None, None
    for choices in itertools.product(*options):
        names = {key: value for choice in choices for key, value in choice.items()}

        def number(value):
            try:
                return f"{float(value):.12g}"
            except (TypeError, ValueError):
                return value

        def normalized(value):
            if isinstance(value, list):
                return [normalized(item) for item in value]
            return names.get(value, number(value))

        regions = {}
        for raw in data.get(":regions", []):
            attributes = {item[0]: item[1:] for item in raw[1:]}
            target = attributes[":target"][0]
            physical = {key: normalized(value) for key, value in sorted(attributes.items()) if key not in {":rgba", ":target"}}
            descriptor = {"target": names.get(target, target), **physical}
            if ":ranges" not in attributes:
                descriptor["xml_site_suffix"] = raw[0]
            regions[target + "_" + raw[0]] = descriptor

        def reference(value):
            if isinstance(value, list):
                return [reference(item) for item in value]
            if value in regions:
                return {"region": regions[value]}
            return names.get(value, number(value))

        key_of = lambda value: json.dumps(value, sort_keys=True, separators=(",", ":"))
        payload = {
            "problem": data.get("problem"),
            "declarations": [[role, kind, len(group)] for (role, kind), group in sorted(groups.items())],
            "regions": sorted(regions.values(), key=key_of),
            "init": sorted([reference(value) for value in data.get(":init", [])], key=key_of),
            "scene_properties": reference(data.get(":scene_properties", [])),
        }
        if include_goal:
            payload["goals"] = sorted([reference(value) for value in goal_atoms(data)], key=key_of)
        serialized = key_of(payload)
        if best_key is None or serialized < best_key:
            best_key, best = serialized, payload
    return best


def physical_signature(text: str, include_goal: bool = True) -> str:
    value = json.dumps(canonical_payload(text, include_goal), sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(value.encode()).hexdigest()


def composition_signature(text: str) -> str:
    data = sections(text)
    value = {
        "problem": data.get("problem"),
        "fixtures": sorted(typed_declarations(data.get(":fixtures", [])).values()),
        "objects": sorted(typed_declarations(data.get(":objects", [])).values()),
    }
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()
