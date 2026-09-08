# Batch91 · Original K3 pair + Goal bowl/cabinet

- `VCN91_001` (3 events, 2200 steps): Turn on the stove, then put the moka pot on the stove, then put the black bowl on top of the cabinet.
- `VCN91_002` (3 events, 2200 steps): Put the black bowl on top of the cabinet, then turn on the stove, then put the moka pot on the stove.
- `VCN91_003` (4 events, 2800 steps): Turn on the stove, then put the moka pot on the stove, then open the top drawer, then put the black bowl in the top drawer.
- `VCN91_004` (4 events, 2800 steps): Open the top drawer, then put the black bowl in the top drawer, then turn on the stove, then put the moka pot on the stove.

Original K3 BDDL explicitly requires Turnon(stove) AND On(moka,stove). Both are retained, in native K3 order. The Goal top-drawer source BDDL only encodes In(bowl,drawer); these new instructions additionally require an explicit native Open milestone before In, but Open is not imposed as an extra final predicate. Remove K3 frying pan only; import Goal cabinet+bowl together at same-index learned robot-frame poses. Screen full object and robot/gripper contacts plus knob/drawer sweeps before inference. Three-event tasks receive2200 steps, four-event tasks2800; seed7, replan8, infer4, intermediateTC>.7 twice, no finalTC. Separate frozen top3 and drawer4 packs permit evaluation overlap without mutating an active benchmark.
