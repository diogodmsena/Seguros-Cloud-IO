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
6. **Docker (A Caixa de Mudança):** Empacota todo o nosso sistema para que funcione na nuvem definitiva (ex: SaveinCloud).
7. **SQLite (O Diário de Bordo):** É o nosso banco de dados fixo e super leve. Ele atua como a memória de longo prazo da nossa IA, lembrando de tudo o que você conversou nos últimos minutos e guardando os seus feedbacks.
8. **Guardrails (O Segurança da Porta):** Um escudo inteligente que intercepta a mensagem *antes* dela chegar no cérebro. Se o cliente tentar pedir coisas proibidas (como "emita minha apólice agora" ou assuntos como "futebol" e "política"), o Segurança barra o acesso e devolve uma resposta padrão protetora, evitando riscos à seguradora.
9. **HuggingFace / Datasets (A Biblioteca Externa):** Importamos grandes arquivos públicos com milhares de perguntas reais do mercado de seguros. Isso dá ao nosso Cérebro um vocabulário e contexto muito maiores do que apenas os nossos próprios PDFs, reduzindo as chances de a IA não saber responder.
10. **Ngrok (O Túnel Seguro):** Uma ponte criptografada que permite que a API na nuvem (SaveinCloud) consulte o motor de IA pesado (Ollama Llama 3.2) rodando no seu computador local. Isso corta drasticamente os custos de GPU na nuvem durante a fase de estudos e desenvolvimento.

---

## 🛤️ Pipeline End-to-End (O Caminho da Mensagem)

Veja o passo a passo exato do que acontece quando um cliente manda um *"Meu seguro auto cobre quebra de vidro?"*:

1. **O Cliente:** Digita a mensagem no chat do site ou no WhatsApp.
2. **Botpress:** Recebe o texto e dispara via HTTP POST para a nossa API hospedada na SaveinCloud (`/api/chat`).
3. **Guardrails (Nuvem):** O Maestro analisa a mensagem instantaneamente. É um xingamento ou assunto proibido? Se sim, barra. Se não, deixa passar.
4. **ChromaDB (Nuvem):** A API busca no banco de dados vetorial quais trechos de PDFs falam sobre "vidros". Ela encontra a "Cláusula 12" do Regulamento Geral.
5. **Ngrok (A Viagem):** A nuvem empacota a Pergunta do Cliente + a Cláusula 12 e manda isso pelo túnel do Ngrok direto para o seu PC local.
6. **Ollama (IA Local):** O modelo Llama 3.2 rodando na sua máquina lê a Cláusula 12 e escreve uma resposta natural, amigável e correta, baseada 100% no documento.
7. **A Entrega:** A resposta gerada volta pelo túnel para a SaveinCloud, que devolve pro Botpress, que exibe na tela do cliente. Tudo em menos de 5 segundos!

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

**4. Deploy em Produção (Docker Compose):**
Para rodar oficialmente na nuvem pela porta web padrão (80):
```bash
docker-compose -f docker-compose.prod.yml up -d --build
```

---

## ✨ Features (Principais Funcionalidades)

- **Zero Alucinação:** A IA é travada e configurada para só responder o que está escrito nos PDFs da seguradora. Se ela não souber, ela passa para um humano.
- **Privacidade Máxima:** Todo o processamento (vetores e Ollama) roda localmente. Os dados dos clientes e os PDFs não vazam para a internet aberta se você não quiser.
- **Multicanal:** Graças ao Botpress, o mesmo cérebro (API) pode responder clientes via Webchat, WhatsApp Empresarial ou Microsoft Teams com zero esforço extra.

---

## 🧠 Como Treinar o seu Robô (Adicionar Conhecimento)

A nossa infraestrutura de nuvem é 100% autônoma. Para adicionar novos documentos ao cérebro do robô, você não precisa acessar servidores. Faça tudo localmente e deixe o GitHub Actions trabalhar:

1. **Adicionar PDFs:** Coloque os arquivos `.pdf` ou `.txt` da sua seguradora dentro da pasta `backend/data/raw_pdfs/`.
2. **Adicionar Perguntas Diretas:** Edite o arquivo `backend/data/faqs.csv` adicionando suas perguntas e respostas.
3. **Enviar para a Nuvem:** No seu terminal ou VS Code, faça o commit e o push:
   ```bash
   git add .
   git commit -m "adicionando nova apolice de vida"
   git push
   ```

**O que acontece depois?** 
A esteira de Deploy do GitHub Action vai jogar seus arquivos na nuvem (SaveinCloud) e vai acionar automaticamente o script de ingestão. O sistema deletará a memória antiga e reconstruirá todo o banco de dados vetorial do zero com os seus novos PDFs, deixando o robô imediatamente mais inteligente!

---

## ⚖️ Licença

Este material foi publicado sob a licença [Atribuição 4.0 Internacional (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/deed.pt_BR).
