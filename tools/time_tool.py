from datetime import datetime

from langchain.tools import tool


@tool
def get_current_time() -> str:
    """Return the current local server time."""
    return datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
