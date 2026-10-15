# Prompt20

Prompt20 is a text-based RPG powered by AI. It uses an AI game master to narrate adventures, manage characters, resolve dice rolls, and save campaign progress.

## Features

- Character creation with different races and classes.
- AI-powered storytelling.
- Dice rolls for uncertain actions.
- Character and campaign state management.
- Save and resume campaigns.
- English and Portuguese language support.

## Requirements

- Python 3.12 or later.
- [uv](https://docs.astral.sh/uv/)
- An OpenRouter API key.

## Setup

1. Clone the repository and enter the project directory.

2. Install dependencies:

   ```bash
   uv sync
   ```

3. Create a `.env` file in the project root:

   ```env
   OPENROUTER_API_KEY=your_api_key_here
   ```

   Get an API key at [OpenRouter](https://openrouter.ai/).

## Run

Start the game with:

```bash
uv run main.py
```

Follow the prompts to create your character and start your adventure.

## Tests

Run the test suite with:

```bash
uv run pytest
```

## Reset

To reset the character and campaign data, run:

```bash
uv run reset_game.py
```

**Warning:** This will clear the saved character and campaign state.
