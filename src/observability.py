import os
from dotenv import load_dotenv
from langfuse.langchain import CallbackHandler

load_dotenv()

LANGFUSE_PUBLIC_KEY = os.getenv("LANGFUSE_PUBLIC_KEY", "")
LANGFUSE_SECRET_KEY = os.getenv("LANGFUSE_SECRET_KEY", "")
LANGFUSE_BASE_URL = os.getenv("LANGFUSE_BASE_URL", "https://jp.cloud.langfuse.com")

# Ensure standard environment variables are set for Langfuse SDK
if LANGFUSE_PUBLIC_KEY:
    os.environ["LANGFUSE_PUBLIC_KEY"] = LANGFUSE_PUBLIC_KEY
if LANGFUSE_SECRET_KEY:
    os.environ["LANGFUSE_SECRET_KEY"] = LANGFUSE_SECRET_KEY
if LANGFUSE_BASE_URL:
    os.environ["LANGFUSE_HOST"] = LANGFUSE_BASE_URL


def get_langfuse_callback() -> CallbackHandler | None:
    """Instantiate and return Langfuse CallbackHandler using environment variables."""
    if LANGFUSE_PUBLIC_KEY and LANGFUSE_SECRET_KEY:
        try:
            return CallbackHandler()
        except Exception as e:
            print(f"[Langfuse Warning] Could not initialize handler: {e}")
            return None
    return None
