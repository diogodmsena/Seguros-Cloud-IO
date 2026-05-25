import sys
import os
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def run_tests():
    print("Iniciando testes funcionais e de tempo de resposta...")
    
    # 1. Pergunta coberta pelos PDFs/FAQs
    start_time = time.time()
    response1 = client.post("/api/chat", json={"message": "Qual é o telefone da central de atendimento?"})
    end_time = time.time()
    
    print(f"\n[Teste 1] Pergunta no contexto (FAQ)")
    print(f"Status: {response1.status_code}")
    print(f"Resposta: {response1.json().get('response') if response1.status_code == 200 else response1.text}")
    print(f"Tempo: {end_time - start_time:.2f}s")
    
    # 2. Pergunta fora do contexto (Fallback)
    start_time = time.time()
    response2 = client.post("/api/chat", json={"message": "Qual é a receita para fazer um bolo de chocolate?"})
    end_time = time.time()
    
    print(f"\n[Teste 2] Pergunta fora do contexto (Fallback esperado)")
    print(f"Status: {response2.status_code}")
    print(f"Resposta: {response2.json().get('response') if response2.status_code == 200 else response2.text}")
    print(f"Tempo: {end_time - start_time:.2f}s")

if __name__ == "__main__":
    try:
        run_tests()
    except Exception as e:
        print(f"Erro ao executar testes: {e}")
