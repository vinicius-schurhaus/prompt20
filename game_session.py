import json

from ai_agent import run_agent_turn, save_campaign
from config import SYSTEM_PROMPT


def start_session(character, game_state, created_character):
    language = character.get("language", "pt")

    if language not in ("pt", "en"):
        language = "pt"

    language_name = {
        "pt": "Portuguese",
        "en": "English",
    }[language]

    system_prompt = (
        SYSTEM_PROMPT
        + "\n\nThe player's selected language is "
        + language_name
        + ".\n\nCurrent saved campaign state:\n"
        + json.dumps(game_state, ensure_ascii=False, indent=2)
    )

    messages = [
        {"role": "system", "content": system_prompt},
    ]

    if game_state.get("story_summary"):
        opening_message = {
            "pt": (
                f"Retome a aventura de {character['name']} a partir "
                "do estado salvo. Não reinicie a história. Descreva "
                "brevemente a situação atual e pergunte o que o "
                "personagem faz."
            ),
            "en": (
                f"Resume {character['name']}'s adventure from the "
                "saved campaign state. Do not restart the story. "
                "Briefly describe the current situation and ask what "
                "the character does."
            ),
        }
    else:
        opening_message = {
            "pt": (
                f"Comece imediatamente a aventura de {character['name']}. "
                "Use a história, a raça e a classe do personagem para "
                "criar a primeira cena. Não peça ao jogador para começar. "
                "Não responda apenas com uma palavra ou título. Apresente "
                "a cena e termine perguntando o que o personagem faz."
            ),
            "en": (
                f"Begin the adventure for {character['name']} immediately. "
                "Use the character's backstory, race, and class to create "
                "the opening scene. Do not ask the player to start. "
                "Do not respond with only a word or title. Present the "
                "scene and end by asking what the character does next."
            ),
        }

    if not created_character:
        print("\n" + "=" * 50 + "\n")

    messages.append(
        {
            "role": "user",
            "content": opening_message[language],
        }
    )

    if not run_agent_turn(messages):
        return

    exit_commands = {
        "pt": {"sair", "encerrar", "exit", "quit"},
        "en": {"exit", "quit"},
    }

    while True:
        try:
            prompt = "\nVocê: \n\n" if language == "pt" else "\nYou: \n\n"
            user_input = input(prompt).strip()

        except (EOFError, KeyboardInterrupt):
            print()
            save_campaign(messages, language)
            break

        if not user_input:
            continue

        if user_input.lower() in exit_commands[language]:
            save_campaign(messages, language)
            break

        messages.append(
            {
                "role": "user",
                "content": user_input,
            }
        )

        if not run_agent_turn(messages):
            print(
                "The response could not be generated. "
                "You can try again or exit the game."
            )
