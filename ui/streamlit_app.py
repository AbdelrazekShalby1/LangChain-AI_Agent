from pathlib import Path
import sys

# ============================================================
# Project Root
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# Imports
# ============================================================

import uuid

import streamlit as st

from langchain.messages import HumanMessage
from langgraph.types import Command

from agents.agent import agent
from services.structured_output import summarize_task
from rag.ingest import ingest_pdf


# ============================================================
# Project Root
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# Streamlit Page Configuration
# ============================================================

st.set_page_config(
    page_title="AI Knowledge & Task Assistant",
    page_icon="🤖",
    layout="wide",
)


# ============================================================
# Header
# ============================================================

st.title("🤖 AI Knowledge & Task Assistant")

st.caption(
    "LangChain Agent + Tools + RAG + Qdrant + Memory + "
    "Summarization + HITL"
)


# ============================================================
# Session State
# ============================================================

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

if "chat" not in st.session_state:
    st.session_state.chat = []

if "pending" not in st.session_state:
    st.session_state.pending = None

if "indexed_files" not in st.session_state:
    st.session_state.indexed_files = set()


# ============================================================
# Agent Config
# ============================================================

config = {
    "configurable": {
        "thread_id": st.session_state.thread_id,
    }
}


# ============================================================
# PDF Upload / Knowledge Base
# ============================================================

st.sidebar.header("📚 Knowledge Base")

uploaded_files = st.sidebar.file_uploader(
    "Upload PDF files",
    type=["pdf"],
    accept_multiple_files=True,
)


if uploaded_files:

    documents_dir = PROJECT_ROOT / "data" / "documents"

    documents_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    for uploaded_file in uploaded_files:

        # Prevent re-indexing the same file
        # during Streamlit reruns.
        if uploaded_file.name in st.session_state.indexed_files:
            continue

        file_path = documents_dir / uploaded_file.name

        # Save uploaded file
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Index the PDF
        with st.spinner(
            f"Indexing {uploaded_file.name}..."
        ):
            count = ingest_pdf(str(file_path))

        # Mark file as indexed
        st.session_state.indexed_files.add(
            uploaded_file.name
        )

        st.sidebar.success(
            f"✅ {uploaded_file.name} "
            f"indexed ({count} chunks)"
        )


# ============================================================
# Sidebar - Conversation
# ============================================================

with st.sidebar:

    st.divider()

    st.subheader("💬 Conversation")

    st.code(
        st.session_state.thread_id,
        language="text",
    )

    if st.button(
        "🆕 New conversation",
        use_container_width=True,
    ):

        st.session_state.thread_id = str(
            uuid.uuid4()
        )

        st.session_state.chat = []

        st.session_state.pending = None

        st.rerun()


# ============================================================
# Sidebar - Structured Output
# ============================================================

with st.sidebar:

    st.divider()

    st.subheader("🧩 Structured Output")

    st.write(
        "Turn a task into a validated Pydantic object."
    )

    if st.button(
        "Summarize last user message",
        use_container_width=True,
    ):

        user_messages = [
            message
            for role, message in st.session_state.chat
            if role == "user"
        ]

        if user_messages:

            with st.spinner(
                "Generating structured output..."
            ):

                summary = summarize_task(
                    user_messages[-1]
                )

            st.json(
                summary.model_dump()
            )

        else:

            st.info(
                "Send a message first."
            )


# ============================================================
# Helper: Extract Last Text
# ============================================================

def extract_last_text(result):

    if not result or "messages" not in result:
        return ""

    for msg in reversed(
        result["messages"]
    ):

        content = getattr(
            msg,
            "content",
            "",
        )

        if (
            isinstance(content, str)
            and content.strip()
        ):

            return content

    return ""


# ============================================================
# Helper: Run Agent
# ============================================================

def run_agent(user_text: str):

    result = agent.invoke(
        {
            "messages": [
                HumanMessage(
                    content=user_text
                )
            ]
        },
        config=config,
    )

    # Human-in-the-loop interrupt
    if "__interrupt__" in result:

        st.session_state.pending = (
            result["__interrupt__"]
        )

        return None

    return extract_last_text(result)


# ============================================================
# Chat History
# ============================================================

for role, content in st.session_state.chat:

    with st.chat_message(role):

        st.markdown(content)


# ============================================================
# Human-in-the-Loop Panel
# ============================================================

if st.session_state.pending:

    st.warning(
        "⏸️ The agent wants to execute "
        "a sensitive tool."
    )

    st.json(
        st.session_state.pending
    )

    col1, col2 = st.columns(2)


    # --------------------------------------------------------
    # Approve
    # --------------------------------------------------------

    with col1:

        if st.button(
            "✅ Approve email",
            use_container_width=True,
        ):

            result = agent.invoke(
                Command(
                    resume={
                        "decisions": [
                            {
                                "type": "approve"
                            }
                        ]
                    }
                ),
                config=config,
            )

            st.session_state.pending = None

            answer = extract_last_text(
                result
            )

            if answer:

                st.session_state.chat.append(
                    (
                        "assistant",
                        answer,
                    )
                )

            st.rerun()


    # --------------------------------------------------------
    # Reject
    # --------------------------------------------------------

    with col2:

        if st.button(
            "❌ Reject email",
            use_container_width=True,
        ):

            result = agent.invoke(
                Command(
                    resume={
                        "decisions": [
                            {
                                "type": "reject",
                                "message": (
                                    "The user rejected "
                                    "this email action."
                                ),
                            }
                        ]
                    }
                ),
                config=config,
            )

            st.session_state.pending = None

            answer = extract_last_text(
                result
            )

            if answer:

                st.session_state.chat.append(
                    (
                        "assistant",
                        answer,
                    )
                )

            st.rerun()


# ============================================================
# Chat Input
# ============================================================

user_input = st.chat_input(
    "Ask something... "
    "e.g. 'Search my documents for RAG' "
    "or 'Send an email...'"
)


# ============================================================
# Handle User Message
# ============================================================

if (
    user_input
    and not st.session_state.pending
):

    # Save user message
    st.session_state.chat.append(
        (
            "user",
            user_input,
        )
    )


    # Display user message
    with st.chat_message("user"):

        st.markdown(
            user_input
        )


    # Run Agent
    with st.chat_message("assistant"):

        with st.spinner(
            "Thinking..."
        ):

            answer = run_agent(
                user_input
            )


        # Normal response
        if answer:

            st.markdown(
                answer
            )

            st.session_state.chat.append(
                (
                    "assistant",
                    answer,
                )
            )


        # HITL interrupt
        else:

            st.info(
                "The agent is paused. "
                "Review the action above."
            )

            st.rerun()