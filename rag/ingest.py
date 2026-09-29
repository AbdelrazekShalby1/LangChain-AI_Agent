from pathlib import Path
from uuid import uuid4

from rag.loaders import load_pdf
from rag.splitter import split_documents
from rag.vectorstore import get_vectorstore


def ingest_pdf(pdf_path: str) -> int:
    documents = load_pdf(pdf_path)
    chunks = split_documents(documents)

    vectorstore = get_vectorstore()
    ids = [str(uuid4()) for _ in chunks]
    vectorstore.add_documents(chunks, ids=ids)

    return len(chunks)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python -m rag.ingest data/documents/my_file.pdf")
        raise SystemExit(1)

    count = ingest_pdf(sys.argv[1])
    print(f"Indexed {count} chunks.")
