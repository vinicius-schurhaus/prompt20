from character_creation import create_character
from reset_game import reset_game
from tools.get_character import get_character
from tools.load_game import load_game


def has_saved_campaign(game_state):
    if not isinstance(game_state, dict) or "error" in game_state:
        return False

    return bool(
        game_state.get("story_summary")
        or game_state.get("active_objectives")
        or game_state.get("known_npcs")
        or game_state.get("important_events")
        or game_state.get("current_location", "Unknown") != "Unknown"
        or game_state.get("campaign_name", "Untitled Adventure") != "Untitled Adventure"
    )


def choose_game_mode(language):
    prompts = {
        "pt": (
            "\nUm jogo salvo foi encontrado.\n"
            "1. Continuar o jogo atual\n"
            "2. Começar um novo jogo\n"
        ),
        "en": (
            "\nA saved game was found.\n"
            "1. Continue the current game\n"
            "2. Start a new game\n"
        ),
    }

    invalid_messages = {
        "pt": "Opção inválida. Digite 1 ou 2.",
        "en": "Invalid choice. Enter 1 or 2.",
    }

    while True:
        print(prompts[language])
        choice = input("> ").strip()

        if choice in ("1", "2"):
            return choice

        print(invalid_messages[language])


def initialize_game():
    character = get_character()
    has_character = "error" not in character and bool(character.get("name"))

    game_state = load_game()

    has_campaign = has_character and has_saved_campaign(game_state)

    if has_campaign:
        language = character.get("language", "pt")

        if language not in ("pt", "en"):
            language = "pt"

        choice = choose_game_mode(language)

        if choice == "1":
            return character, game_state, False

        game_state = reset_game()
        character = create_character()

        return character, game_state, True

    if has_character:
        if "error" in game_state:
            game_state = reset_game()

        return character, game_state, False

    game_state = reset_game()
    character = create_character()

    return character, game_state, True
