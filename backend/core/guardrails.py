import re

def check_guardrails(message: str) -> dict:
    """
    Verifica se a mensagem do usuário fere alguma regra de negócio (guardrails).
    Retorna um dicionário com o status de bloqueio e a mensagem de resposta padrão se bloqueado.
    """
    message_lower = message.lower()

    # 1. Bloqueio de assuntos não relacionados a seguros
    # Uma heurística simples (para o MVP)
    out_of_scope_keywords = ["receita de bolo", "política", "futebol", "religião", "jogos", "filmes", "clima", "tempo"]
    if any(word in message_lower for word in out_of_scope_keywords):
        return {
            "blocked": True,
            "reason": "out_of_scope",
            "message": "Desculpe, sou um assistente especializado em seguros corporativos. Como posso ajudar você em relação à sua apólice ou dúvidas sobre os nossos produtos?"
        }

    # 2. Prevenção de Promessas Indevidas (Emissão / Indenização imediata)
    risk_keywords = [r"emiti.*apólice.*agora", r"aprov.*indenização", r"pagar.*sinistro.*hoje"]
    for pattern in risk_keywords:
        if re.search(pattern, message_lower):
            return {
                "blocked": True,
                "reason": "unauthorized_promise",
                "message": "Entendo a sua necessidade. No entanto, emissão de apólices, aprovação de indenizações ou pagamentos exigem validação de um analista humano especializado. Deseja que eu transfira você para um corretor?"
            }
            
    # 3. Bloqueio de fornecimento de dados sensíveis diretos sem autenticação (LGPD / Segurança)
    # Exemplo: O usuário pedindo "qual o CPF" ou "qual o cartão" na base.
    sensitive_keywords = ["qual meu cpf", "qual meu cartão", "dados do cartão"]
    if any(word in message_lower for word in sensitive_keywords):
        return {
            "blocked": True,
            "reason": "lgpd_data_request",
            "message": "Por questões de segurança e privacidade (LGPD), não tenho acesso a dados sensíveis ou informações financeiras pessoais sem uma autenticação formal. Para acessar sua conta, por favor faça login no portal oficial do cliente."
        }

    return {"blocked": False}
