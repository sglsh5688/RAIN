# COMPOSE_350

- Instruction: Put the right moka pot on the stove, then put the left moka pot on the stove, and finally turn on the stove.
- Family: `X13_kitchen8_two_moka_then_turn_on`
- Physical group: `libero10_kitchen8_stove_off_at_init`
- Semantic components: `3`
- Pure original-atomic composition: `true`

## Components

1. Put the right moka pot on the stove — `on(moka_pot_1, flat_stove_1_cook_region)`
2. Put the left moka pot on the stove — `on(moka_pot_2, flat_stove_1_cook_region)`
3. Turn on the stove — `turnon(flat_stove_1)`

## Notes

- The source's initially-on stove state is removed so the turn-on clause is not true at reset.
- The interaction mask is flat_stove_1_button only; the whole stove is forbidden as fallback.
