# Chatbot Inteligente para Seguros (RAG API)

> Um assistente virtual inteligente capaz de ler documentos complexos (como apólices de seguro) e responder dúvidas de clientes de forma humana, rápida e precisa.

---

## 📖 O Que é Este Projeto?

Imagine que você tem milhares de páginas de PDFs sobre regras de seguros. Quando um cliente pergunta: *"O meu seguro cobre quebra de vidro?"*, encontrar essa resposta manualmente é lento. 

Este projeto constrói um **Cérebro Digital** que lê a sua pergunta, vasculha instantaneamente todos os documentos de seguros armazenados, encontra a regra exata e escreve uma resposta natural para o cliente, sem inventar informações. Isso é feito usando uma técnica avançada chamada **RAG (Geração Aumentada por Recuperação)**.

---

## 🧩 Como Funciona?

Para que essa mágica aconteça, conectamos várias tecnologias modernas como se fossem engrenagens de um relógio:

1. **FastAPI (O Maestro):** É o servidor que fica "escutando". Ele é a porta de entrada que recebe a mensagem do usuário e gerencia qual ferramenta deve ser chamada a seguir.
2. **ChromaDB (A Biblioteca Mágica):** É um banco de dados especial (vetorial). Em vez de guardar as palavras exatas do PDF, ele guarda o **significado** delas.
3. **LangChain (O Intérprete):** É a ferramenta que conecta a pesquisa feita no ChromaDB com a Inteligência Artificial, entregando o conteúdo "mastigado".
4. **Ollama / OpenAI (O Cérebro):** É a IA que lê a pergunta do cliente + os trechos e formula uma resposta educada e natural.
5. **Botpress (A Vitrine):** É a interface visual (a tela do chat). Ele repassa a mensagem do cliente para o nosso Maestro.
6. **Ngrok (O Túnel):** Cria um túnel secreto ligando o seu computador à internet aberta, para que o Botpress consiga se comunicar.
7. **Docker (A Caixa de Mudança):** Empacota todo o nosso sistema para que funcione na nuvem definitiva (ex: SaveinCloud).
8. **SQLite (O Diário de Bordo):** É o nosso banco de dados fixo e super leve. Ele atua como a memória de longo prazo da nossa IA, lembrando de tudo o que você conversou nos últimos minutos e guardando os seus feedbacks.
9. **Guardrails (O Segurança da Porta):** Um escudo inteligente que intercepta a mensagem *antes* dela chegar no cérebro. Se o cliente tentar pedir coisas proibidas (como "emita minha apólice agora" ou assuntos como "futebol" e "política"), o Segurança barra o acesso e devolve uma resposta padrão protetora, evitando riscos à seguradora.
10. **HuggingFace / Datasets (A Biblioteca Externa):** Importamos grandes arquivos públicos com milhares de perguntas reais do mercado de seguros. Isso dá ao nosso Cérebro um vocabulário e contexto muito maiores do que apenas os nossos próprios PDFs, reduzindo as chances de a IA não saber responder.
---

## 🚀 Quick Start (Como Rodar o Projeto)

Se você for um desenvolvedor e quiser ligar este robô no seu computador, o processo é super simples:

**1. Instale as dependências:**
```bash
pip install -r requirements.txt
```

**2. Inicie o Servidor (Maestro):**
```bash
python backend/main.py
```

**3. Teste a Interface Local:**
Abra o seu navegador de internet e acesse: `http://localhost:8000/`. Você verá uma interface de chat escura e elegante, já integrada com o sistema.

**4. Abra para a Internet (Ngrok):**
Em um novo terminal, rode o comando abaixo para gerar o link público:
```bash
ngrok http 8000
```
*(Lembre-se de colocar esse link gerado lá nas configurações do seu Botpress!)*

---

## ✨ Features (Principais Funcionalidades)

- **Zero Alucinação:** A IA é travada e configurada para só responder o que está escrito nos PDFs da seguradora. Se ela não souber, ela passa para um humano.
- **Privacidade Máxima:** Todo o processamento (vetores e Ollama) roda localmente. Os dados dos clientes e os PDFs não vazam para a internet aberta se você não quiser.
- **Multicanal:** Graças ao Botpress, o mesmo cérebro (API) pode responder clientes via Webchat, WhatsApp Empresarial ou Microsoft Teams com zero esforço extra.

---

## ⚖️ Licença

Uso Privado - Seguros Cloud IO. Todos os direitos reservados.
