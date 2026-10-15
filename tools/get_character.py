import json
from pathlib import Path

CHARACTER_FILE = Path(__file__).resolve().parent.parent / "data" / "character.json"


def get_character() -> dict:
    try:
        with CHARACTER_FILE.open("r", encoding="utf-8") as file:
            return json.load(file)

    except (OSError, json.JSONDecodeError) as e:
        return {"error": f"Failed to load character: {e}"}


schema_get_character = {
    "type": "function",
    "function": {
        "name": "get_character",
        "description": (
            "Retrieve the current character sheet, including name, "
            "backstory, race, class, level, health, attributes, and inventory."
        ),
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
}
