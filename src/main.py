"""
FastAPI REST Server — Enterprise RBAC RAG API.
Provides endpoints for role-filtered RAG querying and admin document lifecycle management.
"""
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from typing import List, Optional

from src.ingester import process_pdf_bytes
from src.retriever import add_texts_to_qdrant
from src.rag_engine import query_rag_chain_with_sources
from src.admin_ops import index_pdf_for_roles, list_indexed_pdfs, delete_pdf_from_index

app = FastAPI(
    title="Enterprise RBAC RAG API",
    description="Production-ready Enterprise RAG API featuring Qdrant Payload-Based RBAC Filtering, Groq LLM Inference & Langfuse Tracing",
    version="1.0.0",
)


class QueryRequest(BaseModel):
    question: str
    user_role: str = "employee"
    k: int = 3


class DeleteDocumentRequest(BaseModel):
    filename: str


@app.get("/")
def root():
    return {
        "status": "online",
        "service": "Enterprise RBAC RAG API",
        "endpoints": [
            "POST /query",
            "POST /admin/index-pdf",
            "GET  /admin/list-pdfs",
            "DELETE /admin/delete-pdf",
        ],
    }


@app.post("/query")
def query_rbac_rag(payload: QueryRequest):
    if not payload.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    try:
        res = query_rag_chain_with_sources(
            question=payload.question,
            user_role=payload.user_role,
            k=payload.k,
        )
        # Format sources for JSON response
        sources = [
            {
                "source": doc.metadata.get("source", "unknown"),
                "page": doc.metadata.get("page", 0) + 1,
                "allowed_roles": doc.metadata.get("allowed_roles", []),
                "content_snippet": doc.page_content[:200] + "...",
            }
            for doc in res["docs"]
        ]
        return {
            "question": payload.question,
            "user_role": payload.user_role,
            "answer": res["answer"],
            "retrieved_sources": sources,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/admin/index-pdf")
async def admin_index_pdf(
    file: UploadFile = File(...),
    allowed_roles: str = Form("employee,hr_manager,payroll_officer,ops_lead,executive"),
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="File must be a PDF")
    try:
        content = await file.read()
        role_list = [r.strip() for r in allowed_roles.split(",") if r.strip()]
        num_chunks = index_pdf_for_roles(content, filename=file.filename, allowed_roles=role_list)
        return {
            "status": "success",
            "filename": file.filename,
            "allowed_roles": role_list,
            "chunks_indexed": num_chunks,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/admin/list-pdfs")
def admin_list_pdfs():
    try:
        indexed = list_indexed_pdfs()
        return {
            "total_documents": len(indexed),
            "documents": indexed,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/admin/delete-pdf")
def admin_delete_pdf(payload: DeleteDocumentRequest):
    try:
        delete_pdf_from_index(payload.filename)
        return {
            "status": "success",
            "message": f"Successfully deleted '{payload.filename}' from vector index.",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
