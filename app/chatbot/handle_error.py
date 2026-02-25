import re
import json
from langchain_core.tools.base import ToolException


def handle_tool_error(error: ToolException):
    error_str = str(error)

    # Extract the 'detail' value inside single quotes
    match = re.search(r"'detail':\s*'([^']+)'", error_str)

    if match:
        return f"{match.group(1)}"

    # Fallback for HTTP status extraction
    http_match = re.search(r"HTTP error (\d+)", error_str)
    if http_match:
        status_code = http_match.group(1)
        return f"Request failed (HTTP {status_code})."

    return "Unable to process your request."
