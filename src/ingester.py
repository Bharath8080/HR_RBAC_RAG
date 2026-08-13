"""
Ingests PDFs into Qdrant with RBAC metadata on every chunk.
Supports Hybrid indexing (Dense + BM25 Sparse) via src/retriever.
"""
import io
from pathlib import Path

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader

from src.retriever import get_qdrant_client, reset_collection_schema, add_documents_to_qdrant

CHUNK_SIZE    = 1000
CHUNK_OVERLAP = 150

DATA_DIR     = Path(__file__).resolve().parent.parent / "data"
PUBLIC_ROLES = ["employee", "hr_manager", "payroll_officer", "ops_lead", "executive"]

# RBAC role mapping for batch re-ingestion
ROLE_MAPPING = {
    "employee_handbook_2026.pdf":               ["employee", "hr_manager", "payroll_officer", "ops_lead", "executive"],
    "performance_and_grievance_policy.pdf":     ["hr_manager", "ops_lead", "executive"],
    "code_of_conduct_and_ethics_policy.pdf":    ["employee", "hr_manager", "payroll_officer", "ops_lead", "executive"],
    "salary_structure_bands_2026.pdf":          ["payroll_officer", "hr_manager", "executive"],
    "bonus_payout_matrix_2026.pdf":             ["payroll_officer", "executive"],
    "health_insurance_plan_2026.pdf":           ["employee", "hr_manager", "payroll_officer", "ops_lead", "executive"],
    "pf_and_gratuity_policy.pdf":               ["payroll_officer", "hr_manager", "executive"],
    "maternity_and_paternity_leave_policy.pdf": ["employee", "hr_manager", "payroll_officer", "ops_lead", "executive"],
    "recruitment_and_onboarding_policy.pdf":    ["employee", "hr_manager", "ops_lead", "executive"],
    "learning_and_development_policy.pdf":      ["employee", "hr_manager", "payroll_officer", "ops_lead", "executive"],
}


def process_pdf_bytes(file_bytes: bytes, filename: str, allowed_roles: list[str] | None = None) -> int:
    """Ingest a single PDF (bytes) into Qdrant. Used by Streamlit UI / FastAPI upload."""
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


def ingest_all_pdfs() -> None:
    """Re-index all enterprise PDFs with Dense + BM25 Sparse vectors and RBAC metadata."""
    client = get_qdrant_client()
    reset_collection_schema(client)

    splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    all_chunks = []

    pdf_files = sorted(DATA_DIR.rglob("*.pdf"))
    print(f"Found {len(pdf_files)} PDFs. Chunking...")

    for pdf_path in pdf_files:
        filename = pdf_path.name
        roles = ROLE_MAPPING.get(filename, PUBLIC_ROLES)

        reader = PdfReader(str(pdf_path))
        pages = []
        for page_num, page in enumerate(reader.pages):
            text = page.extract_text()
            if text and text.strip():
                pages.append(Document(
                    page_content=text,
                    metadata={"source": filename, "page": page_num, "allowed_roles": roles},
                ))

        chunks = splitter.split_documents(pages)
        all_chunks.extend(chunks)
        print(f"  • {filename:<50} → {len(chunks):>3} chunks | roles: {', '.join(roles)}")

    print(f"\nIndexing {len(all_chunks)} chunks (Dense + BM25 Sparse)...")
    add_documents_to_qdrant(all_chunks)
    print("Done! Hybrid index is ready.\n")


if __name__ == "__main__":
    ingest_all_pdfs()
