# Batch 1 design rules

- Gripper/end-effector trajectory continuity is a soft ranking prior, never a hard exclusion rule.
- Paired order controls are included in the same source-aligned physical scene.
- All required object and fixture root poses remain source-aligned. Only task-required drawer joints change.
- Every task passes five-state collision, initial-goal, articulation, mask, and replay validation before inference.
- Success is ordered native goal completion; Compose final termination has no TC gate.
