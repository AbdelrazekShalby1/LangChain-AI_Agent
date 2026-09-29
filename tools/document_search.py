from langchain.tools import tool

from rag.retriever import search_documents


@tool
def search_knowledge_base(query: str) -> str:
    """Search the project's uploaded documents and return relevant passages."""
    docs = search_documents(query, k=4)

    if not docs:
        return "No relevant documents were found."

    parts = []
    for i, doc in enumerate(docs, start=1):
        source = doc.metadata.get("source", "unknown")
        page = doc.metadata.get("page", "?")
        parts.append(
            f"[Source {i}] {source} | page={page}\n{doc.page_content}"
        )

    return "\n\n".join(parts)
