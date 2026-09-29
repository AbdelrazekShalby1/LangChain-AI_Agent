from langchain_groq import ChatGroq

from config import GROQ_API_KEY, GROQ_MODEL
from models import TaskSummary


def summarize_task(text: str) -> TaskSummary:
    """Separate structured-output example.

    It intentionally uses a plain model call instead of the tool-using agent.
    This keeps the example compatible with providers that restrict combining
    structured output and streaming/tool calls in the same request.
    """
    model = ChatGroq(
        api_key=GROQ_API_KEY,
        model=GROQ_MODEL,
        temperature=0,
    )

    structured_model = model.with_structured_output(TaskSummary)

    return structured_model.invoke(
        f"Convert this user request into the TaskSummary schema:\n\n{text}"
    )
