import random
import re


def roll_dice(notation: str) -> dict:
    match = re.fullmatch(r"\s*(\d+)\s*[dD]\s*(\d+)\s*", notation)

    if not match:
        return {"error": "Invalid notation. Use the NdX format, such as 1d20."}

    num_dice, num_sides = map(int, match.groups())

    if num_dice < 1 or num_sides < 1:
        return {"error": "The number of dice and sides must be positive."}

    if num_dice > 100:
        return {"error": "The maximum number of dice per roll is 100."}

    rolls = [random.randint(1, num_sides) for _ in range(num_dice)]

    return {
        "notation": f"{num_dice}d{num_sides}",
        "rolls": rolls,
        "total": sum(rolls),
    }


schema_roll_dice = {
    "type": "function",
    "function": {
        "name": "roll_dice",
        "description": (
            "Roll one or more dice using the NdX notation. "
            "Use this function when a dice roll is required during gameplay."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "notation": {
                    "type": "string",
                    "description": "Dice notation, such as 1d20, 2d6, or 4d8.",
                },
            },
            "required": ["notation"],
        },
    },
}
