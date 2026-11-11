"""Read a board-game move that may hold several actions, with Zuse's hosted API.

Step 1 asks one yes/no question per action (and which card was played) in one request.
Step 2 asks, for each action that was found and takes a target, which tile it targets.

    export BINERIC_API_KEY=...        # from platform.bineric.com
    python multi_part_moves.py [zuse-9b|zuse-27b]

Standard library only. The game, its actions and the moves are made up.
"""
import json
import os
import sys
import urllib.request

MODEL = sys.argv[1] if len(sys.argv) > 1 else "zuse-9b"
URL = "https://api.bineric.com/v1/zuse"
THRESHOLD = 0.5  # a yes/no answer above this counts as part of the move

# Each action with a short description. The description helps more than a long instruction.
ACTIONS = {
    "gather": "collect resources",
    "build": "construct a building",
    "move": "move a unit to another tile, not as part of an attack",
    "attack": "attack a unit or a tile",
    "trade": "exchange cards or resources",
}
TARGETED = {"move", "build", "attack"}  # actions that take a tile

GAME = {
    "hand": ["Forest", "Quarry", "Market"],
    "units": {"knight": "B3", "archer": "D1"},
    "tiles": ["B3", "C4", "D1", "D2"],
}

MOVES = [
    "I play the Forest card to gather wood, then move my knight to C4.",
    "I move my archer to D2.",
    "Market card: trade two wood for one stone.",
    "Quarry for stone, build a tower on B3 and attack D1 with my knight.",
    "I pass.",
]


def ask(state, questions):
    body = json.dumps({"model": MODEL, "state": state, "questions": questions}).encode()
    req = urllib.request.Request(URL, body, {"Authorization": f"Bearer {os.environ['BINERIC_API_KEY']}",
                                             "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())["answers"]


def read_move(sentence):
    # The game state goes in as JSON, so the options can be limited to what is legal right now.
    state = {**GAME, "move": sentence}

    # Step 1: one yes/no question per action, plus the card. A "none" option lets Zuse say a card is missing.
    step1 = {a: {"type": "noul", "instructions": f"Does the player's move include the action '{a}' ({d})?"}
             for a, d in ACTIONS.items()}
    step1["card"] = {"type": "choice", "instructions": "Which card does the player play?",
                     "criteria": {**{c: None for c in GAME["hand"]}, "none": "no card is played"}}
    a1 = ask(state, step1)
    actions = [a for a in ACTIONS if a1[a]["noul"] > THRESHOLD]

    # Step 2: the target of each action that was found, one question per action.
    step2 = {f"{a}_tile": {"type": "choice", "instructions": f"Which tile does the '{a}' action target?",
                           "criteria": {**{t: None for t in GAME["tiles"]}, "none": "no tile is targeted"}}
             for a in actions if a in TARGETED}
    a2 = ask(state, step2) if step2 else {}

    return {
        "move": sentence,
        "actions": {a: round(a1[a]["noul"], 2) for a in ACTIONS},
        "found": actions,
        "card": [a1["card"]["choice"], round(a1["card"]["confidence"], 2)],
        "tiles": {k: [v["choice"], round(v["confidence"], 2)] for k, v in a2.items()},
    }


if __name__ == "__main__":
    for m in MOVES:
        print(json.dumps(read_move(m), ensure_ascii=False))
