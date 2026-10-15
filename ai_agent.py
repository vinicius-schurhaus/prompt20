import json
import re

from openai import OpenAI, OpenAIError

from tools.get_character import get_character, schema_get_character
from tools.load_game import load_game, schema_load_game
from tools.roll_dice import roll_dice, schema_roll_dice
from tools.save_game import save_game, schema_save_game
from tools.update_character import (
    update_character,
    schema_update_character,
)

MODEL = "openrouter/free"
MAX_ITERATIONS = 20

client = None

AVAILABLE_FUNCTIONS = [
    schema_roll_dice,
    schema_get_character,
    schema_update_character,
    schema_save_game,
    schema_load_game,
]

FUNCTION_MAP = {
    "roll_dice": roll_dice,
    "get_character": get_character,
    "update_character": update_character,
    "save_game": save_game,
    "load_game": load_game,
}

EMOJI_PATTERN = re.compile(
    "["
    "\U0001f000-\U0001faff"
    "\U00002600-\U000027bf"
    "\U0001fc00-\U0001ffff"
    "]|[\ufe0e\ufe0f\u200d]"
)


def initialize_agent(api_key):
    global client

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )


def clean_output(text):
    if not text:
        return ""

    text = EMOJI_PATTERN.sub("", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"\*\*?|\_\_?|\~\~|`", "", text)
    text = re.sub(r"(?m)^\s{0,3}#{1,6}\s*", "", text)
    text = re.sub(r"(?m)^\s*[-*+]\s+", "", text)

    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n[ \t]+", "\n", text)
    text = text.strip()

    lines = text.split("\n")
    formatted_lines = []

    for line in lines:
        line = line.strip()

        if not line:
            if formatted_lines and formatted_lines[-1] != "":
                formatted_lines.append("")
            continue

        is_dialogue = re.match(r"^[^:\n]{1,60}:\s+\S", line)

        if is_dialogue and formatted_lines and formatted_lines[-1] != "":
            formatted_lines.append("")

        formatted_lines.append(line)

    return "\n".join(formatted_lines).strip()


def call_function(tool_call):
    function_name = tool_call.function.name

    if function_name not in FUNCTION_MAP:
        result = {"error": f"Unknown function: {function_name}"}
    else:
        try:
            arguments = json.loads(tool_call.function.arguments)
            result = FUNCTION_MAP[function_name](**arguments)
        except (
            json.JSONDecodeError,
            TypeError,
            ValueError,
        ) as error:
            result = {"error": f"Invalid function call: {error}"}
        except Exception as error:
            result = {"error": f"Function execution failed: {error}"}

    return {
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": json.dumps(result, ensure_ascii=False),
    }


def run_agent_turn(messages):
    if client is None:
        raise RuntimeError("The AI agent has not been initialized.")

    for _ in range(MAX_ITERATIONS):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                tools=AVAILABLE_FUNCTIONS,
            )
        except OpenAIError as error:
            print(f"API error: {error}")
            return False

        message = response.choices[0].message
        messages.append(message.model_dump(exclude_none=True))

        if not message.tool_calls:
            output = clean_output(message.content or "")
            if output:
                print(output)
            return True

        for tool_call in message.tool_calls:
            messages.append(call_function(tool_call))

    print("Error: Maximum number of iterations reached.")
    return False


def save_campaign(messages, language):
    save_messages = list(messages)
    save_messages.append(
        {
            "role": "user",
            "content": (
                "The player is ending this session. Update and save the "
                "complete campaign state using the save_game tool. "
                "Summarize events from this session, preserve established "
                "facts and unresolved objectives, and include the current "
                "location, important NPCs, and important events. "
                "Do not narrate the story. Save the complete updated state."
            ),
        }
    )

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=save_messages,
            tools=[schema_save_game],
            tool_choice={
                "type": "function",
                "function": {"name": "save_game"},
            },
        )
    except OpenAIError as error:
        print(f"Could not save campaign: {error}")
        return False

    message = response.choices[0].message

    if not message.tool_calls:
        print("The model did not call save_game.")
        return False

    saved = False

    for tool_call in message.tool_calls:
        if tool_call.function.name != "save_game":
            continue

        result_message = call_function(tool_call)
        result = json.loads(result_message["content"])

        if result.get("success") is True:
            saved = True
        else:
            print("Could not save campaign: " f"{result.get('error', 'Unknown error')}")

    if saved:
        print(
            {
                "pt": "Campanha salva.",
                "en": "Campaign saved.",
            }.get(language, "Campanha salva.")
        )

    return saved
