
import json
from src.stock_tool import get_stock_info

# Test stock data retrieval.
result = get_stock_info("فولاد")
assert isinstance(result, dict)

# Test serialization for a API tool result.
tool_result = {
    "type": "tool_result",
    "tool_use_id": "actual_tool_call_id",
    "content": json.dumps(result, ensure_ascii=False),
}
assert isinstance(tool_result["content"], str)
print(json.dumps(tool_result, ensure_ascii=False, indent=2))

# Test invalid symbol handling.
try:
    get_stock_info("XYZ123")
except ValueError:
    print("Invalid symbol handled correctly.")
