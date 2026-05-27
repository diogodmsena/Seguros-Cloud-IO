from typing import List
import os
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from backend.core.config import settings


class RAGService:
    def __init__(self):
        self._vector_store = None

    @property
    def vector_store(self):
        if self._vector_store is None:
            # Só inicializa se o diretório do Chroma existir e tiver arquivos
            if (
                os.path.exists(settings.CHROMA_DB_DIR)
                and len(os.listdir(settings.CHROMA_DB_DIR)) > 0
            ):
                embeddings = OllamaEmbeddings(
                    base_url=settings.OLLAMA_BASE_URL, model=settings.OLLAMA_EMBED_MODEL
                )
                self._vector_store = Chroma(
                    persist_directory=settings.CHROMA_DB_DIR,
                    embedding_function=embeddings,
                )
            else:
                print("ChromaDB ainda não foi inicializado/populado.")
        return self._vector_store

    def search_similar_documents(self, query: str, k: int = 3) -> List[str]:
        """
        Busca os k trechos mais relevantes no ChromaDB baseado na similaridade com a query.
        """
        store = self.vector_store
        if store is None:
            return []
        try:
            results = store.similarity_search(query, k=k)
            return [doc.page_content for doc in results]
        except Exception as e:
            print(f"Erro ao buscar no ChromaDB: {e}")
            return []


rag_service = RAGService()
