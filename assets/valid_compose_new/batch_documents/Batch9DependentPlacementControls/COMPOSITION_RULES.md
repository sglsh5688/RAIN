# LIBERO Composition candidate rules

## Category definition

A Composition candidate asks the policy to execute two or three semantic tasks in one episode.  Final task identity is
`physical scene + frozenset(final goal atoms)`; swapping sentence order does not create another candidate.  One explicit,
dependency-safe action order is stored only as the rollout realization.

## Enumeration and exclusions

- Goal: start from the audited 37 compatible two-task edges.  Do not recreate those existing LIBERO-EX tasks; enumerate all
  68 size-three cliques instead.
- Spatial: retain each original bowl-to-plate task, then append every available single extension and every compatible pair
  from `open middle drawer`, `turn on stove`, `second bowl -> cabinet top`, `second bowl -> stove`, and `cookies box -> stove`.
  Any extension already true in the source init is removed.
- LIBERO-10: enumerate every 3-object basket subset in Scenes 1/2, all 3! mug/plate bijections, and the six explicitly
  requested kitchen/study continuations.
- Object: each stock layout has six food objects, so all `C(6,3)=20` triples are generated for all ten layouts: 200 tasks.
- Incompatible final destinations for one object, paraphrases, reverse order, original LIBERO-40 tasks, and existing
  LIBERO-EX composition tasks are not new candidates.

## Pure versus mixed candidates

`pure_composition=true` means every atomic component was explicitly demonstrated in LIBERO-40.  Requested transfers such as
a distractor cookies box onto the stove, the red distractor mug, microwave-top placement, or turn-off are retained but tagged
`pure_composition=false`, so final selection can avoid category confounding if desired.

## Temporal success

Ordinary tasks use the original TC rule: unordered final conjunction.  Two on/off tasks additionally carry ordered
`sequence_stages`.  `off -> on -> off` cannot receive credit from its final state alone, and the two-moka task must place both
pots while the stove is on before the later turn-off.

## Masks and videos

Every low-level action has an exact current-simulator target.  Repeated instances (`plate_1/2/3`, moka pots, two bowls) are
never unioned.  Table-region placement masks are projected from the current BDDL.  Evaluation records only successful videos,
capped at five per task.

## Candidate counts

| Family | Count |
|---|---:|
        | `same_drawer_insert_then_close` | 3 |
| `insertion_then_sibling_open` | 1 |
| `drawer_then_knob_control` | 1 |
| `knob_control_then_cabinet_placement` | 1 |
| `cabinet_placement_then_control` | 1 |
| `stove_placement_then_drawer_control` | 2 |
| `stove_placement_then_knob_control` | 2 |
| `plate_placement_then_control` | 1 |

**Total: 12 tasks / 60 five-episode trials.**
