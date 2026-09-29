# AI Knowledge & Task Assistant

A medium-level LangChain project that combines:

- `create_agent`
- LangChain messages
- custom tools
- tool calling
- Qdrant RAG
- Hugging Face embeddings
- checkpoint memory
- `thread_id`
- `SummarizationMiddleware`
- `HumanInTheLoopMiddleware`
- `Command(resume=...)`
- structured output with Pydantic
- streaming
- batch + `max_concurrency`
- Streamlit UI
- basic tests

## 1. Create the environment

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### Linux/macOS

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 2. Configure environment variables

Copy:

```text
.env.example
```

to:

```text
.env
```

Then add your Groq API key.

The default model is:

```text
openai/gpt-oss-120b
```

Groq currently lists this model as a production model with tool use and structured-output support.

## 3. Qdrant

You have two options.

### Option A: Local Qdrant

Leave `QDRANT_URL` empty.

The project uses:

```text
.qdrant/
```

as a local persistent Qdrant store.

### Option B: Qdrant Cloud

Set:

```env
QDRANT_URL=https://YOUR-CLUSTER-URL
QDRANT_API_KEY=YOUR_API_KEY
```

The project uses the `knowledge_base` collection by default.

## 4. Add documents

Put PDF files inside:

```text
data/documents/
```

Then index each PDF:

```bash
python -m rag.ingest data/documents/my_file.pdf
```

The pipeline is:

PDF
-> PyPDFLoader
-> RecursiveCharacterTextSplitter
-> Hugging Face embeddings
-> Qdrant

The default embedding model is:

```text
sentence-transformers/all-mpnet-base-v2
```

It produces 768-dimensional embeddings.

## 5. Run the application

```bash
streamlit run app.py
```

Open the URL printed by Streamlit.

## 6. Try these prompts

### Normal chat

```text
Explain what RAG is.
```

### Calculator

```text
Calculate (1500 * 0.15) + 200
```

### RAG

```text
Search my documents and explain the main idea of chapter 2.
```

### Weather

```text
What's the weather in Cairo?
```

### Time

```text
What time is it?
```

### HITL

```text
Send an email to john@example.com with subject "Meeting"
and body "Let's meet tomorrow at 10 AM."
```

The agent will pause before executing `send_email`.

The Streamlit UI then shows Approve/Reject buttons.

## 7. Test batch

From Python:

```python
from services.batch import batch_answer

questions = [
    "What is RAG?",
    "What is an agent?",
    "What is a vector database?",
]

answers = batch_answer(questions, max_concurrency=3)

for answer in answers:
    print(answer.content)
```

## 8. Test streaming

```python
from services.streaming import stream_answer

for chunk in stream_answer("Explain LangChain in simple terms."):
    print(chunk.content, end="", flush=True)
```

## 9. Test structured output

```python
from services.structured_output import summarize_task

result = summarize_task(
    "Build a RAG chatbot for university PDF documents."
)

print(result.model_dump())
```

Example shape:

```json
{
  "title": "University PDF RAG chatbot",
  "summary": "Build a chatbot that answers questions from university PDFs.",
  "priority": "medium",
  "next_steps": [
    "Load PDFs",
    "Split documents",
    "Create embeddings",
    "Store vectors in Qdrant"
  ]
}
```

## Architecture

```text
                    ┌─────────────────────┐
                    │     Streamlit UI    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   LangChain Agent   │
                    │    create_agent     │
                    └──────────┬──────────┘
                               │
             ┌─────────────────┼──────────────────┐
             │                 │                  │
             ▼                 ▼                  ▼
        Tools              Memory              Middleware
             │                 │                  │
      ┌──────┼──────┐      thread_id       ┌──────┴──────┐
      │      │      │                       │             │
 Calculator Weather Email             Summarization    HITL
                    │
                    ▼
             ┌─────────────┐
             │    RAG      │
             └──────┬──────┘
                    │
          ┌─────────┴─────────┐
          ▼                   ▼
     Embeddings             Qdrant
          │                   │
          └───────► Search ◄──┘
```

## Important production notes

- `InMemorySaver` is for learning/local development. It loses state when the process stops.
- Replace mock email/weather tools with real integrations only after adding authentication and security.
- For production, use a persistent LangGraph checkpointer.
- Add authentication before exposing the Streamlit app publicly.
- Add document IDs and metadata filters if the system needs per-user or per-file retrieval.
