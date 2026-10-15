import json
from pathlib import Path

GAME_STATE_FILE = Path(__file__).resolve().parent.parent / "data" / "game_state.json"


def load_game() -> dict:
    try:
        with GAME_STATE_FILE.open("r", encoding="utf-8") as file:
            game_state = json.load(file)

        if not isinstance(game_state, dict):
            return {"error": "Invalid game state format."}

        return game_state

    except FileNotFoundError:
        return {"error": "No saved game found."}

    except (OSError, json.JSONDecodeError) as e:
        return {"error": f"Failed to load game: {e}"}


schema_load_game = {
    "type": "function",
    "function": {
        "name": "load_game",
        "description": (
            "Load the previously saved adventure state. Use this tool "
            "when resuming a saved game or when the current game state "
            "needs to be retrieved."
        ),
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
}
