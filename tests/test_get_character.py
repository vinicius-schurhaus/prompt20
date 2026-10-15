import json

from tools import get_character as character_module


def test_get_character_returns_saved_data(tmp_path, monkeypatch):
    character_file = tmp_path / "character.json"
    expected = {
        "name": "Test Hero",
        "backstory": "A wandering adventurer.",
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
    }

    character_file.write_text(
        json.dumps(expected),
        encoding="utf-8",
    )

    monkeypatch.setattr(
        character_module,
        "CHARACTER_FILE",
        character_file,
    )

    assert character_module.get_character() == expected


def test_get_character_handles_missing_file(tmp_path, monkeypatch):
    monkeypatch.setattr(
        character_module,
        "CHARACTER_FILE",
        tmp_path / "missing.json",
    )

    result = character_module.get_character()

    assert "error" in result
    assert result["error"].startswith("Failed to load character:")


def test_get_character_handles_invalid_json(tmp_path, monkeypatch):
    character_file = tmp_path / "character.json"
    character_file.write_text("{invalid json", encoding="utf-8")

    monkeypatch.setattr(
        character_module,
        "CHARACTER_FILE",
        character_file,
    )

    result = character_module.get_character()

    assert "error" in result
