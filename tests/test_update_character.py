import json

from tools import update_character as character_module


def test_update_character_saves_value(tmp_path, monkeypatch):
    character_file = tmp_path / "character.json"
    original = {
        "name": "Test Hero",
        "backstory": "A wandering adventurer.",
        "race": "human",
        "class": "warrior",
        "level": 1,
        "health": 12,
        "attributes": {
            "strength": 3,
            "intelligence": 1,
            "agility": 2,
        },
        "inventory": [],
    }

    character_file.write_text(
        json.dumps(original),
        encoding="utf-8",
    )

    monkeypatch.setattr(
        character_module,
        "CHARACTER_FILE",
        character_file,
    )

    result = character_module.update_character("level", 2)
    saved_data = json.loads(character_file.read_text(encoding="utf-8"))

    assert result["success"] is True
    assert result["updated_field"] == "level"
    assert result["updated_value"] == 2
    assert saved_data["level"] == 2
    assert saved_data["name"] == "Test Hero"


def test_update_character_updates_attributes(tmp_path, monkeypatch):
    character_file = tmp_path / "character.json"
    original = {
        "name": "Test Hero",
        "attributes": {
            "strength": 3,
            "intelligence": 1,
            "agility": 2,
        },
    }

    character_file.write_text(
        json.dumps(original),
        encoding="utf-8",
    )

    monkeypatch.setattr(
        character_module,
        "CHARACTER_FILE",
        character_file,
    )

    new_attributes = {
        "strength": 4,
        "intelligence": 1,
        "agility": 2,
    }

    result = character_module.update_character(
        "attributes",
        new_attributes,
    )

    saved_data = json.loads(character_file.read_text(encoding="utf-8"))

    assert result["success"] is True
    assert saved_data["attributes"] == new_attributes


def test_update_character_allows_any_existing_field(tmp_path, monkeypatch):
    character_file = tmp_path / "character.json"
    original = {
        "name": "Test Hero",
        "custom_field": "old value",
    }

    character_file.write_text(
        json.dumps(original),
        encoding="utf-8",
    )

    monkeypatch.setattr(
        character_module,
        "CHARACTER_FILE",
        character_file,
    )

    result = character_module.update_character(
        "custom_field",
        "new value",
    )

    saved_data = json.loads(character_file.read_text(encoding="utf-8"))

    assert result["success"] is True
    assert saved_data["custom_field"] == "new value"


def test_update_character_rejects_missing_field(tmp_path, monkeypatch):
    character_file = tmp_path / "character.json"
    character_file.write_text(
        json.dumps({"name": "Test Hero"}),
        encoding="utf-8",
    )

    monkeypatch.setattr(
        character_module,
        "CHARACTER_FILE",
        character_file,
    )

    result = character_module.update_character("health", 10)

    assert "error" in result
    assert "health" in result["error"]


def test_update_character_handles_missing_file(tmp_path, monkeypatch):
    monkeypatch.setattr(
        character_module,
        "CHARACTER_FILE",
        tmp_path / "missing.json",
    )

    result = character_module.update_character("name", "Test Hero")

    assert "error" in result
    assert result["error"].startswith("Failed to update character:")


def test_update_character_handles_invalid_json(tmp_path, monkeypatch):
    character_file = tmp_path / "character.json"
    character_file.write_text("{invalid json", encoding="utf-8")

    monkeypatch.setattr(
        character_module,
        "CHARACTER_FILE",
        character_file,
    )

    result = character_module.update_character("name", "Test Hero")

    assert "error" in result
    assert result["error"].startswith("Failed to update character:")
