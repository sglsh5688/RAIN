"""New-only fixed drainer pose and food-fit diagnostics for two-step tasks.

These functions do not change old section tasks, native sites, collision
geometry, or success predicates.  Both destination compartments remain fixed
throughout an episode; only the task's requested active mask may change.
"""

from __future__ import annotations

from pathlib import Path
import xml.etree.ElementTree as ET
import numpy as np

from novel_feedback_fixture_geometry import collision_boxes, quat_matrix
from bowl_drainer_sections_geometry import install_floor_drainer_support, _body_ids, _inner_env


ASSET_ROOT = Path("/path/to/libero_assets")
DRAINER_XML = ASSET_ROOT / "turbosquid_objects/bowl_drainer/bowl_drainer.xml"
ORIGINAL_BASKET_XY = (0.0, 0.26)
FIXED_DRAINER_ROOT_XYZ = (0.0, 0.25471, 0.00602)
LEFT_REGION = "bowl_drainer_1_left_region"
RIGHT_REGION = "bowl_drainer_1_right_region"
COMPARTMENT_TARGETS = {
    "left": dict(native_region=LEFT_REGION, local_site_xyz=(0.0, 0.06211, 0.06757),
                 world_site_xyz=(0.0, 0.31682, 0.07359)),
    "right": dict(native_region=RIGHT_REGION, local_site_xyz=(0.0, -0.05153, 0.06757),
                  world_site_xyz=(0.0, 0.20318, 0.07359)),
}
OBJECT_KINDS = (
    "alphabet_soup", "cream_cheese", "salad_dressing", "bbq_sauce", "ketchup",
    "tomato_sauce", "butter", "milk", "chocolate_pudding", "orange_juice",
)


def fixture_center():
    return FIXED_DRAINER_ROOT_XYZ[:2]


def target_region(side):
    return COMPARTMENT_TARGETS[side]["native_region"]


def nominal_source_rotation(kind):
    """Class-default rotation only, not a claim about saved demonstration poses."""
    quarter = 2**-0.5
    rx = quat_matrix((quarter, quarter, 0, 0))
    rz = quat_matrix((quarter, 0, 0, quarter))
    if kind in ("alphabet_soup", "tomato_sauce"):
        return rz
    if kind in ("cream_cheese", "butter", "chocolate_pudding"):
        return np.eye(3)
    if kind == "bbq_sauce":
        return rx
    if kind in ("salad_dressing", "ketchup", "milk", "orange_juice"):
        return rz @ rx
    raise KeyError(kind)


def object_static_fit(kind, rotation=None):
    """Conservative collision-envelope fit at a supported centered placement.

    A tall bottle protruding above the rim is not intrinsically impossible:
    horizontal fit, native root inclusion, and full-volume inclusion are
    reported separately.  Native In is never replaced by this diagnostic.
    """
    rotation = nominal_source_rotation(kind) if rotation is None else np.asarray(rotation)
    assert rotation.shape == (3, 3) and np.allclose(rotation.T @ rotation, np.eye(3), atol=1e-8)
    object_xml = ASSET_ROOT / "stable_hope_objects" / kind / f"{kind}.xml"
    boxes = collision_boxes(object_xml)
    corners = np.concatenate([box["corners"] @ rotation.T for box in boxes])
    low, high = corners.min(0), corners.max(0)
    horizontal_center = (low[:2]+high[:2])/2
    drainer_boxes = collision_boxes(DRAINER_XML)
    floor = min(drainer_boxes, key=lambda box: box["center"][2])
    floor_top = float(floor["upper"][2])
    root = ET.parse(DRAINER_XML).find("./worldbody/body/body[@name='object']")
    reports = {}
    for side in ("left", "right"):
        site = root.find(f"./site[@name='{side}_region']")
        site_pos = np.fromstring(site.get("pos"), sep=" ")
        site_rotation = quat_matrix(np.fromstring(site.get("quat"), sep=" "))
        half = np.abs(site_rotation @ np.fromstring(site.get("size"), sep=" "))
        object_root = np.array([site_pos[0]-horizontal_center[0], site_pos[1]-horizontal_center[1],
                                floor_top-low[2]+.0002])
        placed = corners+object_root
        margins = np.minimum(placed.min(0)-(site_pos-half), (site_pos+half)-placed.max(0))
        point_margin = np.minimum(object_root-(site_pos-half), (site_pos+half)-object_root)
        reports[side] = dict(
            horizontal_collision_envelope_fits=bool(np.all(margins[:2] >= 0)),
            whole_collision_envelope_fits_native_site=bool(np.all(margins >= 0)),
            object_root_inside_native_site=bool(np.all(point_margin > 0)),
            minimum_margin_xyz_m=margins.tolist(),
            top_protrusion_above_native_site_m=max(0., float(placed.max(0)[2]-(site_pos+half)[2])),
            supported_object_root_local_xyz=object_root.tolist(),
            supported_object_root_world_xyz=(object_root+np.asarray(FIXED_DRAINER_ROOT_XYZ)).tolist(),
        )
    return dict(object_kind=kind, placement_rotation_matrix=rotation.tolist(),
                collision_envelope_xyz_m=(high-low).tolist(), compartments=reports)


def static_report():
    foods = {kind: object_static_fit(kind) for kind in OBJECT_KINDS}
    # A witness option only: do not silently rotate the pickup initialization.
    foods["bbq_sauce"]["upright_identity_diagnostic_alternative"] = object_static_fit("bbq_sauce", np.eye(3))
    return dict(
        fixed_drainer_root_world_xyz=FIXED_DRAINER_ROOT_XYZ,
        original_basket_center_xy=ORIGINAL_BASKET_XY,
        compartment_targets=COMPARTMENT_TARGETS,
        selected_center_offsets_from_original_y_m={
            side: round(values["world_site_xyz"][1]-.26, 8)
            for side, values in COMPARTMENT_TARGETS.items()
        },
        old_centered_root_y_026_would_give_site_centers_y_m={"left": .32211, "right": .20847},
        fixture_motion_during_episode_allowed=False,
        object_fits=foods,
        native_root_success_does_not_certify_release_or_stable_support=True,
    )


def validate_scene(env, metadata):
    """Read-only production-init gate for the common, immobile two-goal scene."""
    from novel_scene_mask_geometry import render_region_mask
    inner = _inner_env(env)
    sim = inner.sim
    left_object, right_object = metadata["left_object"], metadata["right_object"]
    assert left_object != right_object
    assert left_object in inner.objects_dict and right_object in inner.objects_dict
    fixture = inner.fixtures_dict["bowl_drainer_1"]
    fixture_id = int(sim.model.body_name2id(fixture.root_body))
    fixture_position = np.asarray(sim.data.body_xpos[fixture_id])
    fixture_rotation = np.asarray(sim.data.body_xmat[fixture_id]).reshape(3, 3)
    assert np.allclose(fixture_position, FIXED_DRAINER_ROOT_XYZ, atol=1e-6), fixture_position
    assert np.allclose(fixture_rotation, np.eye(3), atol=1e-6), fixture_rotation
    floor_id = int(sim.model.geom_name2id("floor"))
    assert abs(float(sim.data.geom_xpos[floor_id][2])) < 1e-6
    robot_id = int(sim.model.body_name2id(inner.robots[0].robot_model.root_body))
    robot_position = np.asarray(sim.data.body_xpos[robot_id])
    robot_rotation = np.asarray(sim.data.body_xmat[robot_id]).reshape(3, 3)
    assert np.allclose(robot_position[:2], (-.6, 0), atol=1e-6)
    assert np.allclose(robot_rotation, np.eye(3), atol=1e-6)
    site_positions = {}
    masks = {}
    bddl_path = Path(inner.bddl_file_name)
    for side in ("left", "right"):
        name = target_region(side)
        site_id = int(sim.model.site_name2id(name))
        position = np.asarray(sim.data.site_xpos[site_id])
        assert np.allclose(position, COMPARTMENT_TARGETS[side]["world_site_xyz"], atol=1e-6)
        site_positions[side] = position.tolist()
        mask = render_region_mask(inner, bddl_path, name)
        assert mask is not None and np.any(mask), f"Empty {side} native site mask"
        masks[side] = mask.astype(bool)
    assert np.any(masks["left"] != masks["right"]), "Compartment masks are identical"
    assert np.any(masks["left"] & ~masks["right"])
    assert np.any(masks["right"] & ~masks["left"])
    truth = {}
    for name in (left_object, right_object):
        truth[name] = {}
        for side in ("left", "right"):
            value = bool(inner._eval_predicate(["in", name, target_region(side)]))
            truth[name][side] = value
            assert not value, f"Initial object already in a compartment: {name}, {side}"
    assert not bool(inner._check_success()), "Initial composed goal is already true"
    drainer_bodies = _body_ids(sim, fixture_id)
    drainer_geoms = set(np.flatnonzero(np.isin(sim.model.geom_bodyid, list(drainer_bodies))))
    object_geoms = {}
    for name, obj in inner.objects_dict.items():
        bodies = _body_ids(sim, sim.model.body_name2id(obj.root_body))
        for geom_id in np.flatnonzero(np.isin(sim.model.geom_bodyid, list(bodies))):
            object_geoms[int(geom_id)] = name
    contacts = []
    for index in range(sim.data.ncon):
        contact = sim.data.contact[index]
        first, second = int(contact.geom1), int(contact.geom2)
        partner = second if first in drainer_geoms else first if second in drainer_geoms else None
        if partner in object_geoms:
            contacts.append(dict(object=object_geoms[partner], penetration_m=max(0., -float(contact.dist))))
    assert not contacts, f"Initial drainer/food interference: {contacts}"
    return dict(passed=True, left_object=left_object, right_object=right_object,
                fixed_fixture_world_xyz=fixture_position.tolist(),
                native_site_world_xyz=site_positions, all_four_initial_in_goals_false=True,
                initial_native_in_values=truth, initial_drainer_object_contacts=contacts,
                native_mask_pixels={side: int(np.count_nonzero(mask)) for side, mask in masks.items()},
                left_only_mask_pixels=int(np.count_nonzero(masks["left"] & ~masks["right"])),
                right_only_mask_pixels=int(np.count_nonzero(masks["right"] & ~masks["left"])),
                robot_left_world_axis=robot_rotation[:, 1].tolist(),
                fixture_moves_between_steps=False, native_sites_and_predicates_unmodified=True)
