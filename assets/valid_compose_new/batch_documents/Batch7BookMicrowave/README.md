# LIBERO Composition — 439 candidate screen

- Candidates: **2**
- Planned evaluation: **10 episodes** (5/task)
- Status: definitions, fixed init states, source comparison PNGs, and exact-mask validation complete; policy inference not run yet
- Rules: [COMPOSITION_RULES.md](COMPOSITION_RULES.md)

## Family counts

| Family | Tasks |
|---|---:|
| `book_then_microwave_close` | 1 |
| `microwave_close_then_book` | 1 |

## Candidate inventory

| ID | Steps | Pure | Instruction | Final goals | Compare |
|---|---:|---|---|---|---|
| `VCN7_001` | 2 | `true` | Put the book in the back compartment of the caddy, then close the microwave door. | `in(black_book_1, desk_caddy_1_back_contain_region); close(microwave_1)` | [PNG](comparison_png/VCN7_001__scene.png) |
| `VCN7_002` | 2 | `true` | Close the microwave door, then put the book in the back compartment of the caddy. | `close(microwave_1); in(black_book_1, desk_caddy_1_back_contain_region)` | [PNG](comparison_png/VCN7_002__masked_scene.png) |
