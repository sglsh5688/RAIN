# VCN1_006

- Instruction: Put the black bowl in the bottom drawer of the white cabinet, then close the middle drawer of the white cabinet.
- Family: `bowl_insert_then_upper_close`
- Physical group: `long4_ordered_drawer_control`
- Semantic components: `2`
- Pure original-atomic composition: `true`

## Components

1. Put the black bowl in the bottom drawer of the white cabinet — `in(akita_black_bowl_1, white_cabinet_1_bottom_region)`
2. Close the middle drawer of the white cabinet — `close(white_cabinet_1_middle_region)`

## Notes

- Gripper trajectory continuity is a soft prior, not an exclusion rule; both action orders are evaluated where defined.
- All movable-object and fixture root poses are source-aligned; only drawer joint openings required by the new task are changed.
- Strict ordered native events and native final goals determine success; Compose final completion has no TC threshold.
