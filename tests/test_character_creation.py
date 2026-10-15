import json

from character_creation import create_character


def setup_character_data(data_dir, classes, races):
    data_dir.mkdir()

    (data_dir / "classes.json").write_text(
        json.dumps(classes),
        encoding="utf-8",
    )
    (data_dir / "races.json").write_text(
        json.dumps(races),
        encoding="utf-8",
    )


def test_create_character_saves_character(monkeypatch, tmp_path):
    data_dir = tmp_path / "data"

    classes = {
        "warrior": {
            "name": {"en": "Warrior", "pt": "Guerreiro"},
            "health": 12,
            "attributes": {
                "strength": 3,
                "intelligence": 1,
                "agility": 2,
            },
        }
    }

    races = {
        "human": {
            "name": {"en": "Human", "pt": "Humano"},
            "attribute_bonus": {"strength": 1},
        }
    }

    setup_character_data(data_dir, classes, races)
    monkeypatch.setattr("character_creation.DATA_DIR", data_dir)

    answers = iter(
        [
            "Test Hero",
            "1",
            "1",
            "A former soldier seeking redemption.",
        ]
    )
    monkeypatch.setattr("builtins.input", lambda _prompt: next(answers))

    character = create_character(language="en")

    assert character == {
        "name": "Test Hero",
        "backstory": "A former soldier seeking redemption.",
        "race": "human",
        "class": "warrior",
        "level": 1,
        "health": 12,
        "attributes": {
            "strength": 4,
            "intelligence": 1,
            "agility": 2,
        },
        "inventory": [],
        "language": "en",
    }

    saved_character = json.loads(
        (data_dir / "character.json").read_text(encoding="utf-8")
    )
    assert saved_character == character


def test_create_character_applies_racial_bonus(monkeypatch, tmp_path):
    data_dir = tmp_path / "data"

    classes = {
        "mage": {
            "name": {"en": "Mage", "pt": "Mago"},
            "health": 8,
            "attributes": {
                "strength": 1,
                "intelligence": 3,
                "agility": 2,
            },
        }
    }

    races = {
        "elf": {
            "name": {"en": "Elf", "pt": "Elfo"},
            "attribute_bonus": {"intelligence": 1},
        }
    }

    setup_character_data(data_dir, classes, races)
    monkeypatch.setattr("character_creation.DATA_DIR", data_dir)

    answers = iter(
        [
            "Arannis",
            "1",
            "1",
            "An apprentice mage.",
        ]
    )
    monkeypatch.setattr("builtins.input", lambda _prompt: next(answers))

    character = create_character(language="en")

    assert character["attributes"] == {
        "strength": 1,
        "intelligence": 4,
        "agility": 2,
    }
    assert character["language"] == "en"


def test_create_character_saves_portuguese_language(monkeypatch, tmp_path):
    data_dir = tmp_path / "data"

    classes = {
        "warrior": {
            "name": {"en": "Warrior", "pt": "Guerreiro"},
            "health": 12,
            "attributes": {
                "strength": 3,
                "intelligence": 1,
                "agility": 2,
            },
        }
    }

    races = {
        "human": {
            "name": {"en": "Human", "pt": "Humano"},
            "attribute_bonus": {"strength": 1},
        }
    }

    setup_character_data(data_dir, classes, races)
    monkeypatch.setattr("character_creation.DATA_DIR", data_dir)

    answers = iter(
        [
            "Herói",
            "1",
            "1",
            "Uma antiga soldada.",
        ]
    )
    monkeypatch.setattr("builtins.input", lambda _prompt: next(answers))

    character = create_character(language="pt")

    assert character["language"] == "pt"

    saved_character = json.loads(
        (data_dir / "character.json").read_text(encoding="utf-8")
    )
    assert saved_character["language"] == "pt"
