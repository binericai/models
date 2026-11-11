# Example: one sentence, several actions

How to read a text that holds several things at once with Zuse, shown on a board game: a player describes a move in one
sentence, and the sentence can contain two or three actions. The full guide to writing questions is in the API documentation:
[Asking good questions](https://bineric.com/platform/docs#zuse-asking).

## Run it

```bash
export BINERIC_API_KEY=...          # from platform.bineric.com
python examples/multi_part_moves.py zuse-9b     # or zuse-27b
```

Standard library only. The game, its actions and the five moves are made up.

## What it does

A single "Which action does the player take?" choice question can't answer this: it picks exactly one option, so on
*"I play the Forest card to gather wood, then move my knight to C4"* it split its answer between the two actions
(Zuse 9B: move 0.63, gather 0.34; Zuse 27B: gather 0.58, move 0.39). The example works in two steps instead:

1. **One yes/no (`noul`) question per possible action**, plus "Which card does the player play?" with a `none` option,
   in one request. The game state goes in as JSON, so the card options are only the cards in hand.
2. **For each action found that takes a target**, "Which tile does the '*action*' action target?", with a `none` option.

## Results

Recorded with the hosted API: [`output-zuse-9b.jsonl`](examples/output-zuse-9b.jsonl),
[`output-zuse-27b.jsonl`](examples/output-zuse-27b.jsonl). Probability of yes per action, Zuse 9B / Zuse 27B:

| Move | gather | build | move | attack | trade | Card | Tile |
|---|---|---|---|---|---|---|---|
| I play the Forest card to gather wood, then move my knight to C4. | **0.92** / **0.95** | 0.07 / 0.17 | **0.95** / **0.94** | 0.14 / 0.07 | 0.08 / 0.20 | Forest | move → C4 |
| I move my archer to D2. | 0.04 / 0.21 | 0.03 / 0.13 | **0.94** / **0.91** | 0.10 / 0.10 | 0.03 / 0.19 | none | move → D2 |
| Market card: trade two wood for one stone. | 0.37 / 0.32 | 0.21 / 0.20 | 0.39 / 0.20 | 0.19 / 0.08 | **0.93** / **0.95** | Market | – |
| Quarry for stone, build a tower on B3 and attack D1 with my knight. | **0.67** / **0.75** | **0.96** / **0.90** | *0.52* / 0.34 | **0.97** / **0.95** | 0.06 / 0.28 | Quarry | build → B3, attack → D1 |
| I pass. | 0.16 / 0.11 | 0.13 / 0.06 | 0.27 / 0.03 | 0.14 / 0.02 | 0.14 / 0.14 | none | – |

*Bold: part of the move. Italic: an uncertain yes.*

The uncertain case: in the three-action sentence the knight does go to D1, but as part of an attack. The option says
`"move": "move a unit to another tile, not as part of an attack"`; without the last part the 9B said yes with 0.79, with it 0.52.
Its follow-up question was unsure too (move → D1, confidence 0.46). So:

- **Use a band, not one cut-off.** Act on clear answers, for example above 0.8 or below 0.3, and let the player or the
  game's rules settle the ones in between.
- **Check the follow-up confidence.** An unsure detail question often means step 1 found something that isn't there.
- **Make overlapping options exclusive** in their descriptions.

At a 0.5 cut-off the 27B got all five moves right, so it is the safer choice for short, ambiguous texts with several parts.

## Cost

A request is billed for the document once, plus the text of each question, so many small questions in one request cost
little more than one. Two steps means two requests, so the document is billed twice. To save the second request, ask the
detail questions in step 1 as well, and only use the ones that belong to the actions you found.

Questions, or examples that don't work as you expect: support@bineric.com.
