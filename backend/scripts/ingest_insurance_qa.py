import os
import sys
import pandas as pd

# Adiciona o diretório raiz ao sys.path para importações funcionarem
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from backend.core.config import settings


def ingest_dataset_1():
    """Ingere o dataset ojassrivastava18/insurance-qa do Kaggle usando kagglehub."""
    print("Carregando dataset ojassrivastava18/insurance-qa via kagglehub...")
    try:
        import kagglehub
        path = kagglehub.dataset_download("ojassrivastava18/insurance-qa")
        csv_path = os.path.join(path, "question_answer.csv")

        if not os.path.exists(csv_path):
            print(f"Arquivo CSV não encontrado em: {csv_path}")
            return []

        df = pd.read_csv(csv_path)
        print(f"Colunas do CSV: {df.columns.tolist()}")
        documents = []

        for index, row in df.iterrows():
            # Limita a 30 registros para evitar sobrecarga no ngrok (rate limit)
            if index >= 30:
                break

            question = row.get("question") or ""
            answer = row.get("answer") or ""

            content = f"Pergunta: {question}\nResposta: {answer}"
            if question.strip() and answer.strip():
                doc = Document(
                    page_content=content,
                    metadata={
                        "source": "ojassrivastava18/insurance-qa",
                        "index": index,
                    },
                )
                documents.append(doc)

        print(f"Carregados {len(documents)} itens de ojassrivastava18/insurance-qa")
        return documents
    except Exception as e:
        print(f"Erro ao carregar ojassrivastava18/insurance-qa: {e}")
        return []


def ingest_dataset_2():
    """Ingere o dataset deccan-ai/insuranceQA-v2 usando pandas."""
    print("Carregando dataset deccan-ai/insuranceQA-v2...")
    try:
        url = "https://huggingface.co/datasets/deccan-ai/insuranceQA-v2/resolve/main/train.jsonl"
        print(f"Lendo JSONL de: {url}")
        df = pd.read_json(url, lines=True)
        documents = []

        print(f"Colunas disponíveis no v2: {df.columns.tolist()}")

        for index, row in df.iterrows():
            # Limita a 30 registros para evitar sobrecarga no ngrok (rate limit)
            if index >= 30:
                break

            q_text = row.get("input") or ""
            a_text = row.get("output") or ""

            if isinstance(a_text, list):
                a_text = " ".join([str(x) for x in a_text])

            content = f"Pergunta: {q_text}\nResposta: {a_text}"
            if q_text.strip() and a_text.strip():
                doc = Document(
                    page_content=content,
                    metadata={"source": "deccan-ai/insuranceQA-v2", "index": index},
                )
                documents.append(doc)

        print(f"Carregados {len(documents)} itens de deccan-ai/insuranceQA-v2")
        return documents
    except Exception as e:
        print(f"Erro ao carregar deccan-ai/insuranceQA-v2: {e}")
        return []


def main():
    all_docs = []

    # Carregar os datasets
    all_docs.extend(ingest_dataset_1())
    all_docs.extend(ingest_dataset_2())

    if not all_docs:
        print("Nenhum dado de QA de seguros foi carregado. Ingestão cancelada.")
        return

    print(
        f"Total de {len(all_docs)} documentos de QA carregados. Dividindo em chunks..."
    )
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    split_docs = text_splitter.split_documents(all_docs)

    embeddings = OllamaEmbeddings(
        base_url=settings.OLLAMA_BASE_URL, model=settings.OLLAMA_EMBED_MODEL
    )

    print(
        f"Gravando/Atualizando ChromaDB em: {settings.CHROMA_DB_DIR} via Ollama ({settings.OLLAMA_EMBED_MODEL})"
    )
    Chroma.from_documents(
        documents=split_docs,
        embedding=embeddings,
        persist_directory=settings.CHROMA_DB_DIR,
    )
    print("Ingestão dos datasets de QA finalizada com sucesso!")


if __name__ == "__main__":
    main()
