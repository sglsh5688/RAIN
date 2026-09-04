# COMPOSE_333

- Instruction: Turn on the first stove, then put the moka pot on the first stove, and finally move the moka pot to the other stove.
- Family: `X10_kitchen3_two_stove_temporal_transfer`
- Physical group: `libero10_kitchen3_two_opposed_stoves_no_frypan`
- Semantic components: `3`
- Pure original-atomic composition: `true`

## Components

1. Turn on the first stove — `turnon(flat_stove_1)`
2. Put the moka pot on the first stove — `on(moka_pot_1, flat_stove_1_cook_region)`
3. Move the moka pot to the other stove — `on(moka_pot_1, flat_stove_2_cook_region)`

## Notes

- The second stove uses the exact opposite-side KITCHEN_SCENE8 stove coordinate and unchanged orientation.
- The frypan is removed because its original pose intersects the added stove footprint.
- Each turn mask names only the requested stove instance's rotary button.
