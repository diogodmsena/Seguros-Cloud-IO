from typing import List
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from backend.core.config import settings


class LLMService:
    def __init__(self):
        self._llm = None

    @property
    def llm(self):
        if self._llm is None:
            self._llm = ChatOllama(
                base_url=settings.OLLAMA_BASE_URL,
                model=settings.OLLAMA_LLM_MODEL,
                temperature=0.0,  # Temperatura zero para consistência máxima
            )
        return self._llm

    def generate_response(self, question: str, context_chunks: List[str], history: List[dict] = None) -> str:
        """
        Gera uma resposta baseada nos trechos recuperados do RAG e histórico da conversa.
        Se nenhum trecho for relevante, aciona o fallback textual básico.
        """
        llm_client = self.llm
        if not llm_client:
            return "Erro no sistema: Ollama não pôde ser inicializado."

        # Se não houver contexto recuperado do RAG
        if not context_chunks:
            return self.get_fallback_response()

        # Construir o contexto em formato legível
        context_text = "\n\n---\n\n".join(context_chunks)

        # Usando o Estilo de Prompt 2 com diretrizes para perguntas genéricas
        system_prompt = (
            "Você é um assistente de suporte de seguros da Seguros Cloud IO.\n"
            "Baseie sua resposta estritamente no Contexto abaixo.\n"
            "Lembre-se também do histórico recente da conversa para entender perguntas de continuação (como 'E sobre o que falamos antes?').\n"
            "Diretrizes adicionais:\n"
            "1. Se o cliente perguntar genericamente se o seguro cobre algo (ex: 'Meu seguro cobre...'), e o contexto referir-se a um plano específico (ex: Auto Premium, Residencial Premium), responda explicando que a cobertura depende do plano e peça para ele confirmar o tipo de seguro (Auto, Residencial, Vida ou Saúde) ou o número da apólice (exemplo: \"Sim, seu plano pode incluir cobertura para isso. Para confirmar, preciso do tipo do seguro ou número da apólice\").\n"
            "2. Se a resposta para a pergunta não puder ser encontrada no Contexto de forma alguma, escreva exatamente a resposta de fallback:\n"
            '"Desculpe, não encontrei essa informação com segurança. Vou encaminhar você para um especialista humano. Por favor, ligue para a nossa central de atendimento no 0800 123 4567."\n\n'
            f"Contexto:\n{context_text}"
        )

        from langchain_core.messages import AIMessage
        messages = [SystemMessage(content=system_prompt)]
        
        if history:
            for msg in history:
                if msg["role"] == "user":
                    messages.append(HumanMessage(content=msg["content"]))
                elif msg["role"] == "bot":
                    messages.append(AIMessage(content=msg["content"]))

        messages.append(HumanMessage(content=question))

        try:
            response = llm_client.invoke(messages)
            content = response.content.strip()
            return content
        except Exception as e:
            print(f"Erro ao chamar Ollama ({settings.OLLAMA_LLM_MODEL}): {e}")
            return "Desculpe, ocorreu um erro interno ao processar sua solicitação. Por favor, tente novamente mais tarde ou ligue para a nossa central no 0800 123 4567."

    def get_fallback_response(self) -> str:
        return "Desculpe, não encontrei essa informação com segurança. Vou encaminhar você para um especialista humano. Por favor, ligue para a nossa central de atendimento no 0800 123 4567."


llm_service = LLMService()
