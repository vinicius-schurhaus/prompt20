# Prompt20

Prompt20 is an AI-powered, text-based RPG where an AI game master narrates adventures, manages characters, and tracks campaign progress.

## Motivation

AI can hallucinate story details and produce non-random dice rolls, making RPG outcomes unreliable. Prompt20 aims to make gameplay more consistent by using actual dice rolls through a tool and saving campaign state to maintain continuity.

## Quick Start

**Requirements:** Python 3.12+, [uv](https://docs.astral.sh/uv/), and an [OpenRouter API key](https://openrouter.ai/).

1. Clone the repository and enter the project directory.
2. Install dependencies:

   ```bash
   uv sync
   ```

3. Create a `.env` file in the project root:

   ```env
   OPENROUTER_API_KEY=your_api_key_here
   ```

4. Start the game:

   ```bash
   uv run main.py
   ```

## Usage

Follow the prompts to select a language and create your character by choosing a name, race, class, and backstory.

Once the adventure begins, describe your character's actions in the terminal. The AI game master narrates the story and uses dice rolls when outcomes are uncertain. Your campaign progress is saved when you exit, allowing you to continue later.

To reset your character and campaign data, run:

```bash
uv run reset_game.py
```

**Warning:** This clears the saved character and campaign state.

## Contributing

Contributions are welcome. To get started:

1. Fork the repository and create a branch for your changes.
2. Install dependencies with `uv sync`.
3. Run the project with `uv run main.py`.
4. Run tests with `uv run pytest`.
5. Submit a pull request describing your changes.
