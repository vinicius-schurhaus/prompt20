from tools.roll_dice import roll_dice


def test_roll_dice_returns_results(monkeypatch):
    results = iter([4, 2, 6])
    monkeypatch.setattr(
        "tools.roll_dice.random.randint",
        lambda _a, _b: next(results),
    )

    result = roll_dice("3d6")

    assert result == {
        "notation": "3d6",
        "rolls": [4, 2, 6],
        "total": 12,
    }


def test_roll_dice_accepts_uppercase_notation(monkeypatch):
    monkeypatch.setattr(
        "tools.roll_dice.random.randint",
        lambda _a, _b: 5,
    )

    result = roll_dice("1D20")

    assert result["notation"] == "1d20"
    assert result["total"] == 5


def test_roll_dice_rejects_invalid_notation():
    assert "error" in roll_dice("invalid")


def test_roll_dice_rejects_malformed_notation():
    for notation in ("2d6d4", "d20", "2d", "2.5d6", ""):
        assert "error" in roll_dice(notation)


def test_roll_dice_rejects_zero_dice():
    assert "error" in roll_dice("0d6")


def test_roll_dice_rejects_zero_sides():
    assert "error" in roll_dice("2d0")


def test_roll_dice_rejects_more_than_100_dice():
    assert "error" in roll_dice("101d6")
