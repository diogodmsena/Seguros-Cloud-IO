import os
import sys

# Ajuste do path para rodar a partir da pasta scripts/
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datasets import load_dataset
from langchain.docstore.document import Document
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from backend.core.config import settings

def ingest_insurance_qa():
    print("Iniciando o download do dataset 'deccan-ai/insuranceQA-v2'...")
    try:
        # Tenta carregar uma fatia pequena (ex: 50 exemplos) para não demorar horas na demonstração
        dataset = load_dataset("deccan-ai/insuranceQA-v2", split="train[:50]")
    except Exception as e:
        print(f"Erro ao carregar o dataset: {e}")
        return

    documents = []
    print("Processando exemplos...")
    for item in dataset:
        # No dataset insuranceQA, as perguntas estão na coluna 'input' 
        # e as respostas na coluna 'output'
        question = item.get("input", "")
        answer = item.get("output", "")
        if not question or not answer:
            continue
        
        content = f"Q: {question}\nA: {answer}"
        # Metadados ajudam a rastrear a origem e podem ser usados para filtragem
        metadata = {"source": "insuranceQA", "type": "faq_public"}
        documents.append(Document(page_content=content, metadata=metadata))

    if not documents:
        print("Nenhum documento processado.")
        return

    print(f"{len(documents)} pares Q&A prontos para ingestão.")

    print("Inicializando embeddings (Ollama)...")
    embeddings = OllamaEmbeddings(
        base_url=settings.OLLAMA_BASE_URL, 
        model=settings.OLLAMA_EMBED_MODEL
    )

    print("Conectando ao ChromaDB...")
    vector_store = Chroma(
        persist_directory=settings.CHROMA_DB_DIR,
        embedding_function=embeddings,
    )

    print("Inserindo documentos e persistindo banco...")
    vector_store.add_documents(documents)
    # No Chroma moderno com o Langchain, ele persiste automaticamente, 
    # mas chamar persist() não faz mal em versões mais antigas.
    if hasattr(vector_store, 'persist'):
        vector_store.persist()

    print("Ingestão concluída com sucesso! O RAG agora possui conhecimento do InsuranceQA.")

if __name__ == "__main__":
    ingest_insurance_qa()
