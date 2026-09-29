from langchain.agents import create_agent
from langchain_groq import ChatGroq

from config import GROQ_API_KEY, GROQ_MODEL
from memory.checkpointer import checkpointer
from tools import ALL_TOOLS
from agents.middleware import build_middleware


SYSTEM_PROMPT = """
You are an AI Knowledge & Task Assistant.

You can:
- answer normal questions,
- calculate arithmetic,
- search uploaded documents,
- check demo weather,
- get the current time,
- read demo emails,
- send demo emails.

Rules:
1. Use the knowledge-base tool when the user asks about information that may
   exist in uploaded documents.
2. Do not invent document facts. If the documents do not contain the answer,
   say so.
3. Before sending an email, use the send_email tool. Human approval is required
   by middleware.
4. Keep answers concise but useful.
5. When citing retrieved documents, mention the source filename and page when
   available.
"""


def build_agent():
    model = ChatGroq(
        api_key=GROQ_API_KEY,
        model=GROQ_MODEL,
        temperature=0,
    )

    return create_agent(
        model=model,
        tools=ALL_TOOLS,
        system_prompt=SYSTEM_PROMPT,
        middleware=build_middleware(),
        checkpointer=checkpointer,
    )


agent = build_agent()
