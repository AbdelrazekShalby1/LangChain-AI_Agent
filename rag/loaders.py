from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document


def load_pdf(path: str | Path) -> list[Document]:
    path = Path(path)
    docs = PyPDFLoader(str(path)).load()

    for doc in docs:
        doc.metadata["source"] = path.name
        doc.metadata["source_path"] = str(path)

    return docs
