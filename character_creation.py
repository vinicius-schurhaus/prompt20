import json
from pathlib import Path

from translations import TRANSLATIONS

DATA_DIR = Path(__file__).parent / "data"


def load_json(filename):
    with (DATA_DIR / filename).open("r", encoding="utf-8") as file:
        return json.load(file)


def choose_option(options, prompt, language):
    text = TRANSLATIONS[language]
    items = list(options.items())

    print(f"\n{prompt}")

    for index, (_, option) in enumerate(items, start=1):
        print(f"{index}. {option['name'][language]}")

    while True:
        choice = input(text["choose_option"]).strip()

        if choice.isdigit():
            index = int(choice) - 1

            if 0 <= index < len(items):
                return items[index][0]

        print(text["invalid_option"])


def create_character(language=None):
    if language is None:
        language = input("Choose language / Escolha o idioma (en/pt): ").strip().lower()

    while language not in TRANSLATIONS:
        language = input("Invalid language / Idioma inválido (en/pt): ").strip().lower()

    text = TRANSLATIONS[language]
    classes = load_json("classes.json")
    races = load_json("races.json")

    name = ""
    while not name:
        name = input(text["character_name"]).strip()

    race_id = choose_option(
        races,
        text["choose_race"],
        language,
    )
    class_id = choose_option(
        classes,
        text["choose_class"],
        language,
    )

    backstory = input(text["backstory"]).strip()

    character_class = classes[class_id]
    race = races[race_id]

    attributes = character_class["attributes"].copy()

    for attribute, bonus in race["attribute_bonus"].items():
        attributes[attribute] += bonus

    character = {
        "name": name,
        "backstory": backstory,
        "race": race_id,
        "class": class_id,
        "level": 1,
        "health": character_class["health"],
        "attributes": attributes,
        "inventory": [],
        "language": language,
    }

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    character_path = DATA_DIR / "character.json"

    with character_path.open("w", encoding="utf-8") as file:
        json.dump(
            character,
            file,
            indent=4,
            ensure_ascii=False,
        )
        file.write("\n")

    print(f"\n{text['character_created']}")
    print("\n" + "=" * 50 + "\n")

    return character


if __name__ == "__main__":
    create_character()
