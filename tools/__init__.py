from .calculator import calculator
from .document_search import search_knowledge_base
from .email import read_email, send_email
from .time_tool import get_current_time
from .weather import get_weather

ALL_TOOLS = [
    calculator,
    get_weather,
    get_current_time,
    search_knowledge_base,
    read_email,
    send_email,
]
