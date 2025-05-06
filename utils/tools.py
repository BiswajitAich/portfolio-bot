from langchain_core.tools import tool
from datetime import datetime

@tool
def check_current_date_and_time() -> str:
    """Returns the current date and time as a formatted string."""
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")
