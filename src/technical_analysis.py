import json
import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from src.stock_tool import get_stock_info

# Load environment variables from the project root.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

# Initialize the OpenRouter client.
api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise ValueError(
        "OPENROUTER_API_KEY is not set. "
        "Please configure it in the project's .env file."
    )

client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1",
)

# Configure the model.
MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")

# Load the tool schema from the schemas directory.
SCHEMA_PATH = PROJECT_ROOT / "schemas" / "schema.json"

with SCHEMA_PATH.open(encoding="utf-8") as file:
    schema = json.load(file)

# Convert the schema to the OpenAI-compatible function calling format.
tools = [
    {
        "type": "function",
        "function": {
            "name": schema["name"],
            "description": schema["description"],
            "parameters": schema["input_schema"],
            "strict": True,
        },
    }
]

# Require the model to retrieve stock data before analyzing it.
SYSTEM_PROMPT = """تو یک تحلیلگر تکنیکال بازار سرمایه ایران هستی.
قوانین:
1. قبل از هر تحلیل، حتماً ابزار get_stock_info را برای نماد مورد نظر صدا بزن.
2. هرگز قیمت، حجم یا ارزش بازار را از حافظه یا حدس خودت نگو؛ فقط از خروجی ابزار استفاده کن.
3. اگر ابزار خطا داد (نماد نامعتبر)، همین را به کاربر بگو و تحلیل نساز.
4. تحلیل را فقط بر اساس داده‌های ابزار بنویس و اگر داده برای نتیجه‌گیری کافی نیست، صریح بگو."""

# Define the user's question.
question = "تحلیل تکنیکال نماد فولاد را بده."
messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": question},
]

# Force the model to call the stock information tool.
response = client.chat.completions.create(
    model=MODEL,
    messages=messages,
    tools=tools,
    tool_choice={
        "type": "function",
        "function": {"name": "get_stock_info"},
    },
)

assistant_message = response.choices[0].message
# Add the assistant response to the conversation history.
messages.append(assistant_message)

# Execute the tool call and return its result to the model.
if not assistant_message.tool_calls:
    raise RuntimeError("The model did not return a tool call.")

for tool_call in assistant_message.tool_calls:
    if tool_call.function.name != "get_stock_info":
        raise ValueError(
            f"Unknown tool requested: {tool_call.function.name}"
        )
    try:
        arguments = json.loads(tool_call.function.arguments)
        result = get_stock_info(**arguments)
        output = json.dumps(
            result,
            ensure_ascii=False,
            allow_nan=False,
        )
    except (ValueError, RuntimeError) as exc:
        output = json.dumps(
            {"error": str(exc)},
            ensure_ascii=False,
        )

    # Send the tool execution result back to the model.
    messages.append(
        {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": output,
        }
    )

# Request the final analysis using the tool result.
final_response = client.chat.completions.create(
    model=MODEL,
    messages=messages,
)

# Display the final response.
print(final_response.choices[0].message.content)
