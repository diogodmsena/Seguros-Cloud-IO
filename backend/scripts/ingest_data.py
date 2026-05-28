import os
import sys
import shutil
import pandas as pd

# Adiciona o diretório raiz ao sys.path para importações funcionarem
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from backend.core.config import settings


def create_sample_data():
    """Cria dados de exemplo para que o sistema funcione imediatamente."""
    os.makedirs(settings.PDFS_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(settings.FAQS_FILE_PATH), exist_ok=True)

    # 1. Criar FAQ CSV de exemplo (sobrescreve sempre para garantir atualizações)
    faq_data = {
        "Pergunta": [
            "Qual é o telefone da central de atendimento?",
            "Como posso solicitar uma segunda via da minha apólice?",
            "O que devo fazer em caso de sinistro de carro?",
            "Como funciona o cancelamento do seguro residencial?",
            "Quais são as coberturas básicas do seguro de vida?",
            "O seguro cobre danos causados por enchentes?",
            "Como agendar uma consulta pelo seguro de saúde?",
            "Qual o prazo de carência do plano de saúde para exames simples?",
            "Meu seguro cobre vidro quebrado?",
            "Meu seguro cobre vidro lateral?",
        ],
        "Resposta": [
            "Nossa central de atendimento atende pelo telefone 0800 123 4567, disponível 24 horas por dia, 7 dias por semana.",
            "Você pode solicitar a segunda via da sua apólice pelo aplicativo da Seguros Cloud IO, na aba 'Minhas Apólices', ou enviando um e-mail para sac@seguroscloud.io.",
            "Em caso de sinistro auto, sinalize a área por segurança, tire fotos do ocorrido, e abra o chamado imediatamente pelo aplicativo ou ligando para 0800 123 4567.",
            "O cancelamento do seguro residencial pode ser solicitado diretamente no painel do cliente no site da seguradora ou entrando em contato com seu corretor.",
            "O seguro de vida cobre morte natural, morte acidental e oferece assistência funeral individual básica.",
            "O plano de seguro Residencial Premium possui cobertura completa contra danos decorrentes de enchentes, alagamentos e tempestades.",
            "Consultas médicas de saúde podem ser agendadas diretamente através do nosso aplicativo na aba 'Rede Credenciada' ou ligando para o consultório parceiro de sua preferência.",
            "O prazo de carência para exames simples no seguro saúde é de 30 dias a partir do início da vigência da apólice.",
            "Sim, seu plano pode incluir cobertura para vidros. Para confirmar, preciso do tipo do seguro (Auto, Residencial, Vida ou Saúde) ou número da apólice.",
            "Sim, seu plano pode incluir cobertura para vidros. Para confirmar, preciso do tipo do seguro (Auto, Residencial, Vida ou Saúde) ou número da apólice.",
        ],
        "Categoria": [
            "Atendimento",
            "Segunda Via",
            "Sinistro",
            "Cancelamento",
            "Vida",
            "Cobertura",
            "Saúde",
            "Saúde",
            "Cobertura",
            "Cobertura",
        ],
    }
    df = pd.DataFrame(faq_data)
    df.to_csv(settings.FAQS_FILE_PATH, index=False, encoding="utf-8")
    print(f"Atualizado arquivo de FAQ de exemplo em: {settings.FAQS_FILE_PATH}")

    # 2. Criar uma apólice fictícia em formato txt para simular PDF se não houver PDFs
    sample_policy_path = os.path.join(
        settings.PDFS_DIR, "Regulamento_Geral_Auto_Premium.txt"
    )
    with open(sample_policy_path, "w", encoding="utf-8") as f:
        f.write(
            "REGULAMENTO GERAL - SEGURO AUTO PREMIUM (SEGUROS CLOUD IO)\n\n"
            "1. COBERTURA DE VIDROS (CLÁUSULA 12)\n"
            "O plano Auto Premium cobre a substituição ou reparo de vidros das portas, do para-brisa e do vidro traseiro em caso de colisão, quebra acidental ou vandalismo. "
            "Importante: Vidros laterais estão 100% cobertos, sujeitos ao pagamento de franquia reduzida descrita na página de contratação.\n\n"
            "2. SINISTRO E ASSISTÊNCIA 24H (CLÁUSULA 15)\n"
            "A assistência 24h oferece guincho com quilometragem ilimitada dentro do território nacional para panes mecânicas ou colisões. "
            "Para acionar, basta ligar no 0800 123 4567.\n\n"
            "3. EXCLUSÕES (O QUE NÃO ESTÁ COBERTO - CLÁUSULA 20)\n"
            "Estão excluídos de qualquer cobertura danos decorrentes de condução sob o efeito de álcool, drogas ou participação em rachas/competições automobilísticas não autorizadas.\n"
        )
    print(f"Atualizado regulamento de exemplo em: {sample_policy_path}")


def ingest():
    print("Iniciando ingestão de dados para o ChromaDB via Ollama...")

    # Limpar banco Chroma anterior para evitar duplicatas e atualizar os dados limpos
    if os.path.exists(settings.CHROMA_DB_DIR):
        shutil.rmtree(settings.CHROMA_DB_DIR)
        print(f"Diretório antigo do ChromaDB limpo em: {settings.CHROMA_DB_DIR}")

    # create_sample_data() # Desativado para não sobrescrever dados reais do usuário

    documents = []

    # A. Carregar FAQs do CSV
    if os.path.exists(settings.FAQS_FILE_PATH):
        print(f"Carregando FAQs do arquivo: {settings.FAQS_FILE_PATH}")
        df = pd.read_csv(settings.FAQS_FILE_PATH, encoding="utf-8")
        for index, row in df.iterrows():
            doc = Document(
                page_content=f"Pergunta: {row['Pergunta']}",
                metadata={
                    "source": "faq", 
                    "category": row["Categoria"],
                    "resposta": row["Resposta"]
                },
            )
            documents.append(doc)

    # B. Carregar PDFs e arquivos de texto do diretório raw_pdfs
    if os.path.exists(settings.PDFS_DIR):
        for file in os.listdir(settings.PDFS_DIR):
            file_path = os.path.join(settings.PDFS_DIR, file)
            if file.endswith(".pdf"):
                print(f"Processando PDF: {file}")
                loader = PyPDFLoader(file_path)
                documents.extend(loader.load())
            elif file.endswith(".txt"):
                print(f"Processando arquivo de texto: {file}")
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                chunks = [c.strip() for c in content.split("\n\n") if c.strip()]
                for i, chunk in enumerate(chunks):
                    doc = Document(
                        page_content=chunk, metadata={"source": file, "chunk": i}
                    )
                    documents.append(doc)

    if not documents:
        print("Nenhum documento encontrado para indexação.")
        return

    # Separar documentos que precisam de split (PDFs) dos que já são atômicos (FAQs)
    docs_to_split = [doc for doc in documents if doc.metadata.get("source") != "faq"]
    faq_docs = [doc for doc in documents if doc.metadata.get("source") == "faq"]

    # Split dos documentos em chunks menores (Apenas PDFs/Textos longos)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    split_docs = text_splitter.split_documents(docs_to_split)
    
    # Junta os chunks divididos com os FAQs intactos
    final_docs = split_docs + faq_docs
    print(f"Documentos preparados: {len(split_docs)} chunks de PDFs/Textos + {len(faq_docs)} FAQs intactas.")

    embeddings = OllamaEmbeddings(
        base_url=settings.OLLAMA_BASE_URL, model=settings.OLLAMA_EMBED_MODEL
    )

    print(
        f"Criando embeddings usando Ollama ({settings.OLLAMA_EMBED_MODEL}) e persistindo no ChromaDB em: {settings.CHROMA_DB_DIR}"
    )
    Chroma.from_documents(
        documents=final_docs,
        embedding=embeddings,
        persist_directory=settings.CHROMA_DB_DIR,
    )
    print("Ingestão concluída com sucesso! ChromaDB local está pronto para uso.")


if __name__ == "__main__":
    ingest()
