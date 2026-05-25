import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    PROJECT_NAME: str = "Chatbot Seguros RAG API (Local Ollama)"

    # Configurações do Ollama
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_LLM_MODEL: str = os.getenv("OLLAMA_LLM_MODEL", "llama3.2")
    OLLAMA_EMBED_MODEL: str = os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text")

    CHROMA_DB_DIR: str = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "data", "chroma"
    )
    FAQS_FILE_PATH: str = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "data", "faqs.csv"
    )
    PDFS_DIR: str = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "data", "raw_pdfs"
    )


settings = Settings()
