from langchain.agents.middleware import (
    HumanInTheLoopMiddleware,
    SummarizationMiddleware,
)
from langchain_groq import ChatGroq

from config import GROQ_API_KEY, GROQ_MODEL


def build_middleware():

    model = ChatGroq(
        api_key=GROQ_API_KEY,
        model=GROQ_MODEL,
        temperature=0,
    )

    return [
        SummarizationMiddleware(
            model=model,
            trigger=("tokens", 6000),
            keep=("messages", 12),
        ),

        HumanInTheLoopMiddleware(
            interrupt_on={
                "send_email": {
                    "allowed_decisions": ["approve", "edit", "reject"]
                },
                "read_email": False,
                "calculator": False,
                "get_weather": False,
                "get_current_time": False,
                "search_knowledge_base": False,
            },
            description_prefix="Email action requires approval",
        ),
    ]