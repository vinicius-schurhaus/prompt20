import json
from pathlib import Path

CHARACTER_FILE = Path(__file__).resolve().parent.parent / "data" / "character.json"


def update_character(field: str, value: str | int | float | dict | list) -> dict:
    try:
        with CHARACTER_FILE.open("r", encoding="utf-8") as file:
            character = json.load(file)

        if field not in character:
            return {"error": f"Field '{field}' does not exist in the character sheet."}

        character[field] = value

        with CHARACTER_FILE.open("w", encoding="utf-8") as file:
            json.dump(character, file, indent=4, ensure_ascii=False)
            file.write("\n")

        return {
            "success": True,
            "updated_field": field,
            "updated_value": value,
        }

    except (OSError, json.JSONDecodeError) as e:
        return {"error": f"Failed to update character: {e}"}


schema_update_character = {
    "type": "function",
    "function": {
        "name": "update_character",
        "description": (
            "Update an existing top-level field of the character sheet. "
            "For nested objects such as attributes, provide the complete object."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "field": {
                    "type": "string",
                    "description": (
                        "The existing top-level character field to update."
                    ),
                },
                "value": {
                    "type": ["string", "integer", "number", "object", "array"],
                    "description": "The new value for the selected field.",
                },
            },
            "required": ["field", "value"],
        },
    },
}
