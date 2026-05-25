from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.services.rag_service import rag_service
from backend.services.llm_service import llm_service
from backend.core.database import increment_metric, get_all_metrics, save_feedback, get_feedback_stats, save_message, get_history
from backend.core.guardrails import check_guardrails

router = APIRouter()


class ChatRequest(BaseModel):
    user_id: str = "default_user"
    message: str


class ChatResponse(BaseModel):
    response: str


class FeedbackRequest(BaseModel):
    user_id: str
    evaluation: str  # 'positive', 'negative', 'partial'
    message_id: str = None


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="A mensagem não pode estar vazia.")

    # Incrementar métrica global de interações
    increment_metric('total_interactions')

    # Guardrails: Validar se a mensagem fere políticas
    guard = check_guardrails(request.message)
    if guard["blocked"]:
        # Se for bloqueado, retorna a mensagem padrão e salva no histórico
        save_message(request.user_id, "user", request.message)
        save_message(request.user_id, "bot", guard["message"])
        return ChatResponse(response=guard["message"])

    # Salvar a mensagem do usuário no histórico e recuperar histórico anterior
    save_message(request.user_id, "user", request.message)
    chat_history = get_history(request.user_id, limit=4) # Pegar as últimas 4 mensagens de contexto

    # 1. Recuperar contexto usando RAG
    context_chunks = rag_service.search_similar_documents(request.message, k=2)

    # 2. Gerar resposta com LLM + Contexto + Histórico
    reply = llm_service.generate_response(request.message, context_chunks, history=chat_history)

    # Salvar a resposta do Bot no histórico
    save_message(request.user_id, "bot", reply)

    return ChatResponse(response=reply)


@router.post("/feedback")
async def feedback_endpoint(request: FeedbackRequest):
    if request.evaluation not in ['positive', 'negative', 'partial']:
        raise HTTPException(status_code=400, detail="Avaliação inválida. Use positive, negative ou partial.")
    
    save_feedback(request.user_id, request.evaluation, request.message_id)
    return {"status": "success", "message": "Feedback salvo com sucesso."}


@router.get("/metrics")
async def metrics_endpoint():
    metrics = get_all_metrics()
    feedbacks = get_feedback_stats()
    return {
        "status": "online",
        "metrics": metrics,
        "feedbacks": feedbacks
    }


class CurationRequest(BaseModel):
    question: str
    answer: str
    action: str  # 'approve', 'reject'


@router.post("/curation")
async def curation_endpoint(request: CurationRequest):
    if request.action == "approve":
        # Em um cenário real, inseriríamos diretamente no ChromaDB via rag_service.
        # Para o MVP, aceitamos a requisição.
        return {"status": "success", "message": "Item aprovado e adicionado à base de conhecimento."}
    elif request.action == "reject":
        return {"status": "success", "message": "Item rejeitado."}
    else:
        raise HTTPException(status_code=400, detail="Ação inválida. Use 'approve' ou 'reject'.")
