"""Process-local support for an either-compartment bowl-drainer target.

The installed asset is not edited.  A transparent bookkeeping site is added
in memory so LIBERO can parse a conventional ``In`` goal, while the predicate
is evaluated as the logical OR of the asset's unchanged native left and right
compartment sites.  The policy target mask is likewise the exact union of the
two native projected sites rather than a box that includes the divider.
"""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import xml.etree.ElementTree as ET

import numpy as np


ANY_SUFFIX = "any_compartment_region"
LEFT_SUFFIX = "left_region"
RIGHT_SUFFIX = "right_region"

# Both native sites have the same orientation and half size.  Their union box
# is only a parser-visible bookkeeping site; success and masks use the exact
# OR of the original sites below.
ANY_SITE_POS = (0.0, 0.00529, 0.06757)
ANY_SITE_QUAT = (0.5, 0.5, -0.5, -0.5)
ANY_SITE_SIZE = (0.10847, 0.05808, 0.09423)


def _attach_any_site(instance) -> None:
    suffix = ANY_SUFFIX
    if suffix in instance._sites:
        raise ValueError(f"duplicate bowl-drainer site: {instance.name}_{suffix}")
    full_name = instance.naming_prefix + suffix
    roots = [instance.get_obj(), instance.worldbody.find("./body/body")]
    if any(root is None for root in roots):
        raise ValueError(f"cannot attach either-compartment site to {instance.name}")
    attributes = dict(
        name=full_name,
        type="box",
        pos=" ".join(f"{value:.12g}" for value in ANY_SITE_POS),
        quat=" ".join(f"{value:.12g}" for value in ANY_SITE_QUAT),
        size=" ".join(f"{value:.12g}" for value in ANY_SITE_SIZE),
        rgba="0 0 0 0",
        group="0",
    )
    for root in roots:
        if root.find(f".//site[@name='{full_name}']") is not None:
            raise ValueError(f"either-compartment site already exists: {full_name}")
        ET.SubElement(root, "site", **attributes)
    instance._sites.append(suffix)


def _install_geometry() -> None:
    # Reuse the audited fixed-fixture z placement already exercised by the
    # bowl-drainer feedback tasks.
    from novel_feedback_fixture_geometry import install_feedback_fixture_geometry

    install_feedback_fixture_geometry()
    from libero.libero.envs.objects import turbosquid_objects

    cls = turbosquid_objects.BowlDrainer
    if getattr(cls.__init__, "_bowl_drainer_anywhere_geometry", False):
        return
    original_init = cls.__init__

    def initialize(self, *args, **kwargs):
        original_init(self, *args, **kwargs)
        _attach_any_site(self)

    initialize._bowl_drainer_anywhere_geometry = True
    cls.__init__ = initialize


def _install_success_or() -> None:
    from libero.libero.envs.object_states.base_object_states import SiteObjectState

    if getattr(SiteObjectState.check_contain, "_bowl_drainer_anywhere_or", False):
        return
    original = SiteObjectState.check_contain

    def check_contain(self, other):
        if not self.object_name.endswith("_" + ANY_SUFFIX):
            return original(self, other)
        parent = self.object_name[: -len("_" + ANY_SUFFIX)]
        left_name = parent + "_" + LEFT_SUFFIX
        right_name = parent + "_" + RIGHT_SUFFIX
        states = self.env.object_states_dict
        if left_name not in states or right_name not in states:
            raise ValueError(
                f"either-compartment goal requires declared native sites: "
                f"{left_name}, {right_name}"
            )
        return bool(original(states[left_name], other) or original(states[right_name], other))

    check_contain._bowl_drainer_anywhere_or = True
    SiteObjectState.check_contain = check_contain


def render_any_compartment_mask(
    env,
    bddl_path: Path,
    full_name: str,
    image_size: int = 320,
    camera_name: str = "agentview",
):
    """Render the exact union of the two unchanged native compartments."""
    from novel_scene_mask_geometry import render_region_mask as current_renderer

    # When installed, ``current_renderer`` is this function.  Retain the
    # original implementation on the wrapper itself to avoid recursion.
    original = getattr(current_renderer, "_bowl_drainer_original_renderer", current_renderer)
    if not full_name.endswith("_" + ANY_SUFFIX):
        return original(env, bddl_path, full_name, image_size, camera_name)
    parent = full_name[: -len("_" + ANY_SUFFIX)]
    left = original(env, bddl_path, parent + "_" + LEFT_SUFFIX, image_size, camera_name)
    right = original(env, bddl_path, parent + "_" + RIGHT_SUFFIX, image_size, camera_name)
    if left is None and right is None:
        return None
    if left is None:
        return np.ascontiguousarray(right)
    if right is None:
        return np.ascontiguousarray(left)
    return np.ascontiguousarray(np.logical_or(left, right).astype(np.uint8))


def _install_mask_renderer() -> None:
    import novel_scene_mask_geometry as geometry

    if getattr(geometry.render_region_mask, "_bowl_drainer_anywhere_mask", False):
        return
    original = geometry.render_region_mask

    def render(env, bddl_path, full_name, image_size=320, camera_name="agentview"):
        if not full_name.endswith("_" + ANY_SUFFIX):
            return original(env, bddl_path, full_name, image_size, camera_name)
        parent = full_name[: -len("_" + ANY_SUFFIX)]
        left = original(env, bddl_path, parent + "_" + LEFT_SUFFIX, image_size, camera_name)
        right = original(env, bddl_path, parent + "_" + RIGHT_SUFFIX, image_size, camera_name)
        if left is None and right is None:
            return None
        if left is None:
            return np.ascontiguousarray(right)
        if right is None:
            return np.ascontiguousarray(left)
        return np.ascontiguousarray(np.logical_or(left, right).astype(np.uint8))

    render._bowl_drainer_anywhere_mask = True
    render._bowl_drainer_original_renderer = original
    geometry.render_region_mask = render


def install_bowl_drainer_anywhere_support() -> None:
    """Install identical geometry, success, and mask behavior in this process."""
    _install_geometry()
    _install_success_or()
    _install_mask_renderer()


def register_object_bindings(action_objects=None):
    """Register the synthetic action ID used only to request the union mask."""
    from novel_feedback_object_bindings import register_object_bindings as register_feedback

    action_objects = register_feedback(action_objects)
    name = "bowl_drainer_1_" + ANY_SUFFIX
    action_objects[name] = deepcopy(
        dict(name=name, body_name=name, body_ids=[], geom_ids=[], segmentable=False)
    )
    return action_objects
