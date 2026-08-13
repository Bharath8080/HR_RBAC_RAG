"""
RAG Engine — builds and executes the RBAC-aware LangChain RAG pipeline.
Filters retrieved documents based on the requesting user's role.
"""
from __future__ import annotations

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.documents import Document
from langchain_groq import ChatGroq

from src.config import GROQ_API_KEY, GROQ_MODEL
from src.retriever import build_retriever
from src.observability import get_langfuse_callback

SYSTEM_PROMPT = """You are an Enterprise HR & Compliance Assistant.

Use ONLY the provided context below to answer the user's question accurately and professionally.
If the context is empty or does not contain enough information for the query, state clearly:
"As per your current role permissions, you do not have access to view this information."

Context:
{context}
"""


def format_docs(docs: list[Document]) -> str:
    if not docs:
        return "No relevant context accessible for your role."
    sections = []
    for idx, doc in enumerate(docs, 1):
        source = doc.metadata.get("source", f"Doc {idx}")
        page = doc.metadata.get("page", None)
        roles = doc.metadata.get("allowed_roles", [])
        header = f"[{source} | Page {page + 1} | Roles: {roles}]" if page is not None else f"[{source} | Roles: {roles}]"
        sections.append(f"{header}\n{doc.page_content}")
    return "\n\n---\n\n".join(sections)


def build_rag_chain(k: int = 3, user_role: str | None = None):
    retriever = build_retriever(k=k, user_role=user_role)

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "{question}"),
    ])

    llm = ChatGroq(
        model=GROQ_MODEL,
        groq_api_key=GROQ_API_KEY,
        temperature=0.1,
    )

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain


def query_rag_chain_with_sources(question: str, user_role: str | None = None, k: int = 3) -> dict:
    """Execute RAG query and return answer along with retrieved source documents."""
    retriever = build_retriever(k=k, user_role=user_role)
    docs = retriever.invoke(question)

    langfuse_handler = get_langfuse_callback()
    config = {}
    if langfuse_handler:
        config["callbacks"] = [langfuse_handler]

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "{question}"),
    ])

    llm = ChatGroq(
        model=GROQ_MODEL,
        groq_api_key=GROQ_API_KEY,
        temperature=0.1,
    )

    context_str = format_docs(docs)
    chain = prompt | llm | StrOutputParser()
    answer = chain.invoke({"context": context_str, "question": question}, config=config)

    return {
        "answer": answer,
        "docs": docs,
        "user_role": user_role or "admin",
    }


def query_rag_chain(question: str, user_role: str | None = None, k: int = 3) -> str:
    """Helper that returns just the answer string."""
    res = query_rag_chain_with_sources(question, user_role=user_role, k=k)
    return res["answer"]
