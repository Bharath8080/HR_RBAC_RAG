"""
Streamlit UI — Enterprise Role-Based Access Control (RBAC) RAG System.
Features: Persona Role Switcher, RBAC Payload Search, Security Retrieval Audit, & Admin PDF Lifecycle Panel.
"""
import streamlit as st

from src.rag_engine import query_rag_chain_with_sources
from src.admin_ops import list_indexed_pdfs, index_pdf_for_roles, delete_pdf_from_index
from src.observability import LANGFUSE_PUBLIC_KEY

st.set_page_config(
    page_title="Enterprise RBAC RAG Assistant",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Role Definitions & Access Rules ──────────────────────────────────────────
ROLE_PROFILES = {
    "Employee": {
        "role_key": "employee",
        "icon": "👤",
        "tier": "Tier 0 (Public)",
        "badge_color": "green",
        "access_desc": "Public handbooks, benefits summary, ethics code, maternity/paternity leave, L&D policy.",
        "allowed_folders": ["policies/handbook", "policies/conduct", "benefits/health", "legal_labour/maternity", "talent/l_and_d"],
    },
    "HR Manager": {
        "role_key": "hr_manager",
        "icon": "💼",
        "tier": "Tier 1 (Internal & Talent)",
        "badge_color": "blue",
        "access_desc": "All employee policies, performance/grievance PIPs, recruitment workflows, PF & gratuity.",
        "allowed_folders": ["policies/*", "benefits/*", "legal_labour/*", "talent/*", "payroll/salary_bands"],
    },
    "Payroll Officer": {
        "role_key": "payroll_officer",
        "icon": "💳",
        "tier": "Tier 2 (Financial Restricted)",
        "badge_color": "orange",
        "access_desc": "Salary bands (L1-L7), bonus payout matrices, PF & gratuity formulas, handbooks.",
        "allowed_folders": ["payroll/*", "benefits/*", "policies/handbook", "policies/conduct"],
    },
    "Ops Lead": {
        "role_key": "ops_lead",
        "icon": "⚙️",
        "tier": "Tier 1 (Operations & Performance)",
        "badge_color": "violet",
        "access_desc": "Performance reviews, PIP roadmaps, recruitment SLAs, handbooks, health plans.",
        "allowed_folders": ["policies/*", "benefits/health", "talent/*"],
    },
    "Executive": {
        "role_key": "executive",
        "icon": "👔",
        "tier": "Tier 2 (Executive Leadership)",
        "badge_color": "red",
        "access_desc": "Full corporate strategy, EBITDA bonus matrices, salary structures, all governance policies.",
        "allowed_folders": ["ALL CORPORATE DATA"],
    },
    "Admin": {
        "role_key": "admin",
        "icon": "👑",
        "tier": "Super Admin (Unrestricted)",
        "badge_color": "rainbow",
        "access_desc": "Full vector DB access + Document Ingestion, Allow-list Modification, and Deletion.",
        "allowed_folders": ["ALL DATA + DB MANAGEMENT"],
    },
}

PRESET_QUERIES = [
    {
        "label": "💰 Salary Bands (L1-L7)",
        "query": "What are the base salary ranges for L1 to L7 job grades and the basic pay percentage?",
        "allowed_for": ["Payroll Officer", "HR Manager", "Executive", "Admin"],
        "restricted_for": ["Employee", "Ops Lead"],
    },
    {
        "label": "📈 Bonus Payout Matrix",
        "query": "What is the corporate EBITDA multiplier matrix and payout schedule for quarterly bonuses?",
        "allowed_for": ["Payroll Officer", "Executive", "Admin"],
        "restricted_for": ["Employee", "HR Manager", "Ops Lead"],
    },
    {
        "label": "📋 PIP & Grievance SLA",
        "query": "What is the 60-day PIP roadmap and what are the SLA timelines for grievance investigation?",
        "allowed_for": ["HR Manager", "Ops Lead", "Executive", "Admin"],
        "restricted_for": ["Employee", "Payroll Officer"],
    },
    {
        "label": "🏖️ PTO & Travel Per Diems",
        "query": "What is the annual PTO accrual rate and the daily travel per diem allowance?",
        "allowed_for": ["Employee", "HR Manager", "Payroll Officer", "Ops Lead", "Executive", "Admin"],
        "restricted_for": [],
    },
    {
        "label": "🏥 Health Insurance Caps",
        "query": "What are the room rent caps and maternity sub-limits under the health insurance policy?",
        "allowed_for": ["Employee", "HR Manager", "Payroll Officer", "Ops Lead", "Executive", "Admin"],
        "restricted_for": [],
    },
]

# ── Session State Initialization ──────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Sidebar: Persona Switcher & Admin Panel ──────────────────────────────────
with st.sidebar:
    st.title("🛡️ Access Control Portal")
    st.markdown("Select an active role to test payload filtering:")

    selected_role_name = st.selectbox(
        "Active User Role:",
        options=list(ROLE_PROFILES.keys()),
        index=0,
    )

    profile = ROLE_PROFILES[selected_role_name]
    st.caption(f"**Security Tier:** {profile['tier']}")
    st.info(f"**Access Scope:** {profile['access_desc']}")

    st.markdown("---")

    # ── Admin Panel (Visible only when Admin is selected) ─────────────────────
    if profile["role_key"] == "admin":
        st.subheader("👑 Admin Document Management")
        admin_tab1, admin_tab2 = st.tabs(["📤 Upload PDF", "📋 Index Directory"])

        with admin_tab1:
            uploaded_file = st.file_uploader("Upload PDF to Index", type=["pdf"])
            role_options = ["employee", "hr_manager", "payroll_officer", "ops_lead", "executive"]
            selected_roles = st.multiselect("Assign Allowed Roles:", role_options, default=["employee"])

            if uploaded_file and st.button("⚡ Index PDF for Selected Roles"):
                with st.spinner("Indexing PDF with RBAC metadata..."):
                    try:
                        bytes_data = uploaded_file.getvalue()
                        num_chunks = index_pdf_for_roles(
                            bytes_data,
                            filename=uploaded_file.name,
                            allowed_roles=selected_roles,
                        )
                        st.success(f"Indexed {num_chunks} chunks for roles: `{selected_roles}`")
                    except Exception as e:
                        st.error(f"Error: {e}")

        with admin_tab2:
            if st.button("🔄 Refresh Indexed Files List"):
                st.rerun()

            indexed_docs = list_indexed_pdfs()
            if indexed_docs:
                st.markdown(f"**{len(indexed_docs)} Documents in Qdrant Vector Store:**")
                for doc_entry in indexed_docs:
                    with st.expander(f"📄 {doc_entry['source']}"):
                        st.write(f"**Allowed Roles:** `{doc_entry['allowed_roles']}`")
                        if st.button(f"🗑️ Delete `{doc_entry['source']}`", key=f"del_{doc_entry['source']}"):
                            delete_pdf_from_index(doc_entry["source"])
                            st.success(f"Deleted `{doc_entry['source']}`!")
                            st.rerun()
            else:
                st.warning("No documents currently indexed.")

        st.markdown("---")

    st.markdown("### ⚙️ Engine Status")
    st.markdown("- **Vector DB:** Qdrant (Local `./qdrant_db`)")
    st.markdown("- **Filtering:** Payload `is_tenant=True` MatchAny")
    st.markdown("- **LLM:** Groq `llama-3.3-70b-versatile`")
    if LANGFUSE_PUBLIC_KEY:
        st.success("🟢 Langfuse Tracing Active")
    else:
        st.warning("🟡 Langfuse Tracing Off")

# ── Main Content Area ─────────────────────────────────────────────────────────
st.title("🛡️ Enterprise RBAC RAG Assistant")
st.caption(f"Authenticated as: **{profile['icon']} {selected_role_name}** | Filtering active: Qdrant payload match on `metadata.allowed_roles` = `{profile['role_key']}`")

# Active Role Banner
top_col1, top_col2 = st.columns([3, 1])
with top_col1:
    st.markdown(f"### Current Role Scope: **{profile['icon']} {selected_role_name}**")
with top_col2:
    st.markdown(f":{profile['badge_color']}[{profile['tier']}]")

st.markdown("---")

# ── Preset Test Prompts ───────────────────────────────────────────────────────
st.markdown("#### 💡 Quick RBAC Test Questions:")
preset_cols = st.columns(len(PRESET_QUERIES))

for idx, preset in enumerate(PRESET_QUERIES):
    with preset_cols[idx]:
        is_allowed = selected_role_name in preset["allowed_for"]
        status_label = "✅ Allowed" if is_allowed else "🔒 Restricted"

        if st.button(f"{preset['label']}\n\n({status_label})", key=f"preset_{idx}"):
            st.session_state.pending_query = preset["query"]

# Handle preset click
query_to_process = None
if "pending_query" in st.session_state:
    query_to_process = st.session_state.pending_query
    del st.session_state.pending_query

# ── Chat History Display ──────────────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if "retrieved_docs" in msg:
            with st.expander("🛡️ Security Audit: Retrieved Chunks"):
                for d_idx, doc in enumerate(msg["retrieved_docs"], 1):
                    src = doc.metadata.get("source", "Unknown")
                    page = doc.metadata.get("page", 0)
                    roles = doc.metadata.get("allowed_roles", [])
                    st.markdown(f"**[{d_idx}] `{src}` (Page {page + 1})** | Roles: `{roles}`")
                    st.caption(doc.page_content[:300] + "...")

# ── User Chat Input ───────────────────────────────────────────────────────────
chat_input_query = st.chat_input("Ask any question about enterprise policies, compensation, or benefits...")

if chat_input_query:
    query_to_process = chat_input_query

if query_to_process:
    # Append user message
    st.session_state.messages.append({
        "role": "user",
        "content": f"[{selected_role_name}] {query_to_process}",
    })
    with st.chat_message("user"):
        st.write(f"[{selected_role_name}] {query_to_process}")

    # Generate assistant answer with RBAC filter
    with st.chat_message("assistant"):
        with st.spinner(f"Querying Qdrant with RBAC filter for role '{profile['role_key']}'..."):
            try:
                res = query_rag_chain_with_sources(
                    question=query_to_process,
                    user_role=profile["role_key"],
                    k=4,
                )

                answer = res["answer"]
                docs = res["docs"]

                st.write(answer)

                if docs:
                    with st.expander("🛡️ Security & Vector Retrieval Audit"):
                        st.markdown(f"**Retrieved {len(docs)} chunks matching payload filter `allowed_roles CONTAINS '{profile['role_key']}'`:**")
                        for d_idx, doc in enumerate(docs, 1):
                            src = doc.metadata.get("source", "Unknown")
                            page = doc.metadata.get("page", 0)
                            roles = doc.metadata.get("allowed_roles", [])
                            st.markdown(f"**[{d_idx}] `{src}` (Page {page + 1})**")
                            st.code(f"Allowed Roles Payload: {roles}")
                            st.caption(doc.page_content)
                else:
                    st.warning(f"🔒 Access Blocked / No context retrieved. Role '{selected_role_name}' does not have permission to view documents matching this query.")

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "retrieved_docs": docs,
                })

            except Exception as e:
                error_text = f"Error: {str(e)}"
                st.error(error_text)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_text,
                })
