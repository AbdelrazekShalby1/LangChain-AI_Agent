from langchain_groq import ChatGroq

from config import GROQ_API_KEY, GROQ_MODEL


def batch_answer(questions: list[str], max_concurrency: int = 4):
    model = ChatGroq(
        api_key=GROQ_API_KEY,
        model=GROQ_MODEL,
        temperature=0,
    )

    return model.batch(
        questions,
        config={"max_concurrency": max_concurrency},
    )
