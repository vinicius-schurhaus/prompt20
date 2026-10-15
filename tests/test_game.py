import json

from tools import load_game as load_module
from tools import save_game as save_module


def test_save_game_persists_state(tmp_path, monkeypatch):
    game_file = tmp_path / "game_state.json"

    monkeypatch.setattr(save_module, "GAME_STATE_FILE", game_file)

    state = {
        "campaign_name": "Test Campaign",
        "current_location": "Forest",
        "story_summary": "The adventure begins.",
        "active_objectives": ["Find the village"],
        "known_npcs": ["Eldric"],
        "important_events": [],
    }

    result = save_module.save_game(state)

    assert result["success"] is True
    assert json.loads(game_file.read_text(encoding="utf-8")) == state


def test_save_game_allows_additional_fields(tmp_path, monkeypatch):
    game_file = tmp_path / "game_state.json"

    monkeypatch.setattr(save_module, "GAME_STATE_FILE", game_file)

    state = {
        "current_location": "Dungeon",
        "weather": "Storm",
        "custom_data": {"key": "value"},
    }

    result = save_module.save_game(state)

    assert result["success"] is True
    assert json.loads(game_file.read_text(encoding="utf-8")) == state


def test_save_game_rejects_non_dictionary():
    result = save_module.save_game([])

    assert "error" in result


def test_load_game_returns_saved_state(tmp_path, monkeypatch):
    game_file = tmp_path / "game_state.json"
    expected = {
        "campaign_name": "Test Campaign",
        "current_location": "Forest",
    }

    game_file.write_text(
        json.dumps(expected),
        encoding="utf-8",
    )

    monkeypatch.setattr(load_module, "GAME_STATE_FILE", game_file)

    assert load_module.load_game() == expected


def test_load_game_handles_missing_file(tmp_path, monkeypatch):
    monkeypatch.setattr(
        load_module,
        "GAME_STATE_FILE",
        tmp_path / "missing.json",
    )

    result = load_module.load_game()

    assert "error" in result
    assert result["error"] == "No saved game found."


def test_load_game_handles_invalid_json(tmp_path, monkeypatch):
    game_file = tmp_path / "game_state.json"
    game_file.write_text("{invalid json", encoding="utf-8")

    monkeypatch.setattr(load_module, "GAME_STATE_FILE", game_file)

    result = load_module.load_game()

    assert "error" in result


def test_load_game_rejects_non_dictionary(tmp_path, monkeypatch):
    game_file = tmp_path / "game_state.json"
    game_file.write_text(json.dumps(["invalid state"]), encoding="utf-8")

    monkeypatch.setattr(load_module, "GAME_STATE_FILE", game_file)

    result = load_module.load_game()

    assert result == {"error": "Invalid game state format."}
