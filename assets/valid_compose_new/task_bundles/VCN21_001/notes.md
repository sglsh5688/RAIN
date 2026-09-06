# VCN21_001

- Instruction: Put the moka pot on the stove, then close the microwave door.
- Family: `moka_place_then_microwave_close`
- Physical group: `pc_k8_k6`
- Semantic components: `2`
- Pure original-atomic composition: `true`

## Components

1. Put the moka pot on the stove — `on(moka_pot_2,flat_stove_1_cook_region)`
2. Close the microwave door — `close(microwave_1)`

## Notes

- Priority milestone: exact K8 moka_pot_2/stove cluster plus exact K6 microwave root/open joint. K8 moka_pot_1 is removed because its pickup lies in the microwave-door neighborhood.
- Five same-index donor states are reconstructed by T_target_robot @ inverse(T_source_robot) @ T_source_entity.
- BDDL sampling regions are reset scaffolding only and never pose authority; arbitrary repair offsets are forbidden.
- Strict ordered native rising events plus all final BDDL predicates; no Compose final TC gate. Intermediate switching remains TC>0.7 for two consecutive progress-head observations.
