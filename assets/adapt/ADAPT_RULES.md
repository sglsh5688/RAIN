# LIBERO Adapt rules

## Category definition

Adapt tests whether one primitive learned in the original LIBERO-40 is reusable after a controlled change of scene, pose, sibling part, exact target, or already-learned object identity. Every candidate is atomic: exactly one goal atom and no action-level `and`.

## Candidate construction

- **A0 selected seeds:** the nine user-selected candidates are retained. `ANLGX_023` is correctly identified as *close middle drawer*; bottom close is tested separately.
- **A1 Object mirror:** all ten LIBERO-Object floor layouts are reflected across `y=0`; basket and every package keep their pairwise clearance.
- **A2 Spatial transfer:** stove-knob control, drawer insertion, and exact sibling-drawer actions are applied inside original Spatial object arrangements.
- **A3 Scene-4 transfer:** black bowl, wine bottle, and learned package objects are rebound to rack, cabinet-top, or exact white-cabinet drawer destinations; open/close primitives are atomic.
- **A4 Scene-5 exact plates:** both plates move to two reachable front slots copied from Scene 6; target identity remains exact.
- **A5 Caddy:** package objects that pass the prior caddy aperture gate are crossed with four exact compartments.
- **A6 Relative placement:** learned objects are placed in current-BDDL left/right regions relative to the Scene-6 plate.
- **A7 Stove control:** the Scene-8 stove starts off and only its knob is exposed to the policy mask.
- **A8 Microwave mirror:** the source microwave at `y=+0.35, yaw=0` is mirrored to `y=-0.35, yaw=pi`. In this scene its front axis is lateral, so the `pi` rotation makes the cavity and open door face the table center instead of exposing the back / swinging off the outer edge. The manipulated object reuses the original Scene-8 left-side moka-pot pickup slot (`x=-0.05, y=+0.25`), keeping even short packages visible and the approach corridor clear. Cups overlapping the new fixture/corridor are removed. Close uses only `microwave_1_microdoorroot`.

## Context and blocker policy

- Preserve the complete source scene by default.
- Remove only an entity that geometrically overlaps a moved fixture or lies on the demonstrated manipulation corridor.
- Never simplify a scene merely to leave the interacting pair.
- Positions are finite donors copied or reflected from original LIBERO layouts; no arbitrary continuous-coordinate sweep is claimed.

## Masks and validation

- Resolve masks from the current simulator; source JSON fallback is forbidden.
- Repeated targets use exact instances and never a union.
- Drawer masks bind exactly top/middle/bottom.
- Stove actions expose the rotary knob only.
- Table-region goals are projected from each current BDDL.
- Build acceptance requires parsable BDDL, five non-success init states, visible nonempty masks, unique physical-init+goal signature, and no exact original LIBERO-40 duplicate.

This build contains **192** accepted candidates. See `REJECTED_CANDIDATES.tsv` for deterministic deduplication exclusions.
