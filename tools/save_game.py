import json
from pathlib import Path

GAME_STATE_FILE = Path(__file__).resolve().parent.parent / "data" / "game_state.json"


def save_game(game_state: dict) -> dict:
    if not isinstance(game_state, dict):
        return {"error": "Game state must be a dictionary."}

    try:
        GAME_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)

        with GAME_STATE_FILE.open("w", encoding="utf-8") as file:
            json.dump(
                game_state,
                file,
                indent=4,
                ensure_ascii=False,
            )
            file.write("\n")

        return {
            "success": True,
            "message": "Game saved successfully.",
        }

    except (OSError, TypeError, ValueError) as error:
        return {"error": f"Failed to save game: {error}"}


schema_save_game = {
    "type": "function",
    "function": {
        "name": "save_game",
        "description": (
            "Save the complete current campaign state to disk. "
            "Include the campaign name, current location, story summary, "
            "active objectives, known NPCs, and important events. "
            "Preserve established facts needed to resume the adventure."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "game_state": {
                    "type": "object",
                    "description": (
                        "The complete campaign state required "
                        "to resume the adventure."
                    ),
                    "additionalProperties": True,
                },
            },
            "required": ["game_state"],
            "additionalProperties": False,
        },
    },
}
