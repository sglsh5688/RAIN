# VCN6_003

- Instruction: Close the middle drawer of the white cabinet, then close the top drawer of the white cabinet.
- Family: `upper_drawer_reverse_pair`
- Physical group: `long4_ordered_drawer_control`
- Semantic components: `2`
- Pure original-atomic composition: `true`

## Components

1. Close the middle drawer of the white cabinet — `close(white_cabinet_1_middle_region)`
2. Close the top drawer of the white cabinet — `close(white_cabinet_1_top_region)`

## Notes

- Gripper trajectory continuity is a soft prior, not an exclusion rule; both action orders are evaluated where defined.
- All movable-object and fixture root poses are source-aligned; only drawer joint openings required by the new task are changed.
- Strict ordered native events and native final goals determine success; Compose final completion has no TC threshold.
