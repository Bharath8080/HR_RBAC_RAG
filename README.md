# 🛡️ HR RBAC RAG — Enterprise Multi-Tenant RAG with Role-Based Access Control

An enterprise-grade Retrieval-Augmented Generation (RAG) system featuring **Multi-Role RBAC security isolation**, **Dense semantic vector search**, and comprehensive CI/CD evaluation powered by **DeepEval & Groq**.

---

## 📊 Current Evaluation Benchmark (50 Q&A Test Cases)

### 📈 Aggregate Metrics (Stage 1 — Dense Semantic Search)

| Metric | Average Score | Pass Rate | Evaluation Result |
|---|:---:|:---:|---|
| **Faithfulness** | **0.96** | **100.00%** (50/50 passed) | 🟢 Flawless factual grounding in retrieved context |
| **Answer Relevancy** | **0.93** | **98.00%** (49/50 passed) | 🟢 Highly pertinent answers aligned with query |
| **Contextual Precision** | **0.78** | **82.00%** (41/50 passed) | 🟡 Strong signal-to-noise ratio in retrieved context |
| **Contextual Recall** | **0.69** | **70.00%** (35/50 passed) | 🟡 Candidate for Stage 2 & 3 hybrid/reranking boost |
| **RBAC Security Isolation** | **1.00** | **100.00%** (28/28 passed) | 🛡️ Zero cross-role data leaks |

### 🎯 Test Case Summary
- **PASSED**: **64.00%** (32 / 50 test cases passed all metric thresholds)
- **FAILED**: **36.00%** (18 / 50 test cases)

---

## 🏗️ Architecture Overview

- **Vector Database**: Qdrant (Local on-disk vector store with payload index partitioning)
- **Embedding Model**: `BAAI/bge-small-en-v1.5` via FastEmbed (384-dimensional dense embeddings)
- **Generation Model**: Llama 3.3 70B Versatile via ChatGroq
- **Evaluation Judge**: Groq SDK with native structured JSON output
- **Multi-Role RBAC**: Strict payload filtering isolating documents across:
  - `Employee` (General policies, benefits, handbook)
  - `HR Manager` (Performance reviews, grievance SLAs, PIP roadmaps)
  - `Payroll Officer` (Salary bands, bonus payouts, tax slabs)
  - `Ops Lead` & `Executive` (Operational SLAs, enterprise audits)
  - `Admin` (Unrestricted access)

---

## 🚀 Quickstart

### 1. Installation
```powershell
uv sync
```

### 2. Environment Setup
Create a `.env` file based on `.env.example`:
```env
GROQ_API_KEY=gsk_your_groq_key
GROQ_MODEL=llama-3.3-70b-versatile
QDRANT_PATH=./qdrant_db
COLLECTION_NAME=pdf_rag
```

### 3. Ingest Enterprise Documents
```powershell
uv run python scripts/generate_enterprise_pdfs.py
uv run python src/ingester.py
```

### 4. Run Benchmark Evaluation (50 Q&A Pairs)
```powershell
uv run python benchmark.py 50
```

### 5. Launch Streamlit UI
```powershell
uv run streamlit run app.py
```
