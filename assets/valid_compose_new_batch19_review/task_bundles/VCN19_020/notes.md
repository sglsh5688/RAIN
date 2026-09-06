# VCN19_020

- Instruction: Open the top drawer of the wooden cabinet, then put the ramekin on the plate.
- Family: `drawer_open_then_ramekin_plate`
- Physical group: `exact_anlgx_092__pick_up_the_ramekin_on_the_cookies_box_and_place_it_on_the_plate`
- Semantic components: `2`
- Pure original-atomic composition: `true`

## Components

1. Open the top drawer of the wooden cabinet — `open(wooden_cabinet_1_top_region)`
2. Put the ramekin on the plate — `on(glazed_rim_porcelain_ramekin_1, plate_1)`

## Notes

- Reverse-order control: top-drawer interaction then the exact source-aligned ramekin-on-cookies-to-plate placement in one unchanged physical scene.
- All final native predicates must be false after evaluator warm-up.
- Strict ordered native rising events plus every final BDDL predicate determine nominal success; final TC is disabled.
- Publication additionally requires deliberate-close telemetry where applicable and manual video allowlisting.
