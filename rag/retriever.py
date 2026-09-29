from rag.vectorstore import get_vectorstore


def search_documents(query: str, k: int = 4):
    vectorstore = get_vectorstore()
    return vectorstore.similarity_search(query, k=k)
