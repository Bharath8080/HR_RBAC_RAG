"""
Ingests a PDF (bytes) into Qdrant with RBAC metadata attached to every chunk.
For admin-controlled ingestion with a custom allow-list, use admin_ops.index_pdf_for_roles().
"""
import io

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader

from src.retriever import add_documents_to_qdrant

CHUNK_SIZE    = 1000
CHUNK_OVERLAP = 150

# Default allow-list for the standard upload flow
PUBLIC_ROLES = ["employee", "hr_manager", "payroll_officer", "ops_lead", "executive"]


def process_pdf_bytes(file_bytes: bytes, filename: str, allowed_roles: list[str] | None = None) -> int:
    if allowed_roles is None:
        allowed_roles = PUBLIC_ROLES

    reader = PdfReader(io.BytesIO(file_bytes))
    pages = []
    for page_num, page in enumerate(reader.pages):
        text = page.extract_text()
        if text and text.strip():
            pages.append(Document(
                page_content=text,
                metadata={"source": filename, "page": page_num, "allowed_roles": allowed_roles},
            ))

    if not pages:
        return 0

    splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    chunks = splitter.split_documents(pages)
    return len(add_documents_to_qdrant(chunks))
