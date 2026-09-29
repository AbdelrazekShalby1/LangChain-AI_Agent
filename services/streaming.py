from config import GROQ_API_KEY, GROQ_MODEL
from langchain_groq import ChatGroq


def stream_answer(text: str):
    model = ChatGroq(
        api_key=GROQ_API_KEY,
        model=GROQ_MODEL,
        temperature=0,
    )

    return model.stream(text)
