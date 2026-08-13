import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY       = os.getenv("GROQ_API_KEY", "")
QDRANT_PATH        = os.getenv("QDRANT_PATH", "./qdrant_db")
COLLECTION_NAME    = os.getenv("COLLECTION_NAME", "pdf_rag")
GROQ_MODEL         = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
CONFIDENT_API_KEY  = os.getenv("CONFIDENT_API_KEY", "")

