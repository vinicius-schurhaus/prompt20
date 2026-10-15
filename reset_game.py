import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
DATA_DIR = ROOT_DIR / "data"

DEFAULT_CHARACTER = {
    "name": "",
    "backstory": "",
    "race": "",
    "class": "",
    "level": 1,
    "health": 0,
    "attributes": {
        "strength": 0,
        "intelligence": 0,
        "agility": 0,
    },
    "inventory": [],
    "language": "pt",
}

DEFAULT_GAME_STATE = {
    "campaign_name": "Untitled Adventure",
    "current_location": "Unknown",
    "story_summary": "",
    "active_objectives": [],
    "known_npcs": [],
    "important_events": [],
}


def reset_file(filename, data):
    path = DATA_DIR / filename

    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
        file.write("\n")


def reset_game():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    reset_file("character.json", DEFAULT_CHARACTER)
    reset_file("game_state.json", DEFAULT_GAME_STATE)

    return DEFAULT_GAME_STATE.copy()


def main():
    try:
        reset_game()
        print("Prompt20 reset successfully.")
        print("Character and campaign state have been cleared.")

    except OSError as error:
        print(f"Reset failed: {error}")


if __name__ == "__main__":
    main()
