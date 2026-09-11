"""Ordered native-goal evaluator for the diverse original-pose compositions."""
import run_composition_revision_evaluator_entry as ordered


def register_bindings():
    ordered.register_bindings()
    objects = ordered.exact.benchmark_support.ACTION_OBJECTS
    objects["moka_pot_1"] = dict(
        name="moka_pot_1_main",
        body_name="moka_pot_1_main",
        body_ids=[0],
        geom_ids=[],
        segmentable=True,
    )
    assert objects["microwave_1"]["body_name"] == "microwave_1_microdoorroot"
    assert objects["white_cabinet_1_bottom_region"]["body_name"] == "white_cabinet_1_cabinet_bottom"
    assert objects["wooden_cabinet_1_middle_region"]["body_name"] == "wooden_cabinet_1_cabinet_middle"
    assert objects["flat_stove_1_cook_region"]["body_name"] == "flat_stove_1_burner"


register_bindings()


if __name__ == "__main__":
    ordered.exact.evaluator.main()
