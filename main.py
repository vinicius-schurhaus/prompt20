import os

from dotenv import load_dotenv

from ai_agent import initialize_agent
from game_manager import initialize_game
from game_session import start_session


def main():
    load_dotenv()

    api_key = os.environ.get("OPENROUTER_API_KEY")

    if not api_key:
        raise RuntimeError(
            "OPENROUTER_API_KEY is not configured. "
            "Add it to your .env file before running the program."
        )

    initialize_agent(api_key)

    character, game_state, created_character = initialize_game()

    start_session(
        character,
        game_state,
        created_character,
    )


if __name__ == "__main__":
    main()
