# VCN6_004

- Instruction: Close the top drawer of the white cabinet, then close the middle drawer of the white cabinet, and finally close the bottom drawer of the white cabinet.
- Family: `top_middle_bottom_order`
- Physical group: `long4_ordered_drawer_control`
- Semantic components: `3`
- Pure original-atomic composition: `true`

## Components

1. Close the top drawer of the white cabinet — `close(white_cabinet_1_top_region)`
2. Close the middle drawer of the white cabinet — `close(white_cabinet_1_middle_region)`
3. Close the bottom drawer of the white cabinet — `close(white_cabinet_1_bottom_region)`

## Notes

- Gripper trajectory continuity is a soft prior, not an exclusion rule; both action orders are evaluated where defined.
- All movable-object and fixture root poses are source-aligned; only drawer joint openings required by the new task are changed.
- Strict ordered native events and native final goals determine success; Compose final completion has no TC threshold.
