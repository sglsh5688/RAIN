# VCN1_010

- Instruction: Put the moka pot on the stove, then close the middle drawer of the white cabinet.
- Family: `moka_then_upper_drawer_close`
- Physical group: `mkdc_ordered_drawer_control`
- Semantic components: `2`
- Pure original-atomic composition: `true`

## Components

1. Put the moka pot on the stove — `on(moka_pot_2, flat_stove_1_cook_region)`
2. Close the middle drawer of the white cabinet — `close(white_cabinet_1_middle_region)`

## Notes

- Gripper trajectory continuity is a soft prior, not an exclusion rule; both action orders are evaluated where defined.
- All movable-object and fixture root poses are source-aligned; only drawer joint openings required by the new task are changed.
- Strict ordered native events and native final goals determine success; Compose final completion has no TC threshold.
