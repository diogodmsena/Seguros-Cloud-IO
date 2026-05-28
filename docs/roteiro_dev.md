# 🛠️ Roteiro Prático: Como Criar seu Próprio Agente (Local)

Bem-vindo! Este documento é um guia passo-a-passo focado em desenvolvedores que desejam clonar esta arquitetura e construir o seu próprio Agente Especialista de Inteligência Artificial rodando **100% na sua máquina local**.

Neste guia, você aprenderá a preparar a máquina, treinar o agente com os seus próprios documentos e conectar a interface web.

---

## ⚙️ Etapa 1: Preparação do Ambiente (Setup)

Para começar, sua máquina precisará de duas coisas essenciais: **Python e Ollama**.

### 1. Inicializando o Ollama (Seu Cérebro Local)
Baixe e instale o [Ollama](https://ollama.com/) na sua máquina. O Ollama é a engine responsável por rodar os Modelos de Linguagem Pesados (LLMs) localmente usando o hardware do seu PC.
No seu terminal, rode os comandos para baixar os modelos que nossa aplicação utiliza:
```bash
# Modelo responsável por criar os vetores matemáticos (Embeddings)
ollama pull nomic-embed-text

# Modelo responsável por ler os dados e conversar com o cliente
ollama pull llama3.2
```

### 2. Instalação das Dependências do Projeto
Clone o repositório na sua máquina, crie um ambiente virtual (recomendado) e instale as bibliotecas Python necessárias:
```bash
git clone <url-do-repositorio>
cd <nome-da-pasta>
python -m venv venv

# Ative o ambiente virtual (No Windows):
venv\Scripts\activate  

# Ou, se estiver no Mac/Linux:
source venv/bin/activate 

# Instale os pacotes:
pip install -r requirements.txt
```

---

## 🧠 Etapa 2: Treinando o Agente (Ingestão de Dados)

O seu agente nasce "vazio". Para transformá-lo em um especialista na sua área (ou área do seu cliente), você precisa alimentá-lo com seus arquivos (PDFs, regras e FAQs).

### 1. Inserindo os seus Documentos
- Coloque os seus arquivos `.pdf` e `.txt` na pasta: `backend/data/raw_pdfs/`.
- Abra o arquivo `backend/data/faqs.csv` e substitua as perguntas lá presentes pelas perguntas e respostas frequentes do seu próprio negócio.

### 2. Rodando a Ingestão Local
Com os arquivos no lugar, abra o terminal na raiz do projeto e execute o script de ingestão. Isso vai ler todos os arquivos, usar o Ollama para calcular os vetores matemáticos e salvar o banco de dados inteligente localmente na sua máquina:
```bash
python backend/scripts/ingest_data.py
```
> **Nota:** Se a execução for bem-sucedida, você notará que a pasta `backend/data/chroma/` foi criada e preenchida com arquivos `.sqlite3`. Essa pasta é literalmente a memória vetorial do seu robô. Guarde-a com carinho!

---

## 🚀 Etapa 3: Subindo o Projeto e as Interfaces

Agora que o cérebro está treinado com os seus dados, é hora de "ligar" a API para conseguir conversar com ele.

### 1. Iniciando o Backend
Na raiz do projeto, inicie o servidor do FastAPI:
```bash
python backend/main.py
```
A API do seu robô estará viva e escutando requisições em `http://localhost:8000/`.

### 2. Interface Web Nativa (Testando o Bot)
Para facilitar o seu teste e garantir que a IA está respondendo corretamente, o projeto já vem com uma interface pronta. 
Abra o seu navegador de internet e simplesmente acesse a raiz da sua API: `http://localhost:8000/`. Você verá a tela de chat do bot e já poderá começar a fazer perguntas referentes aos PDFs que você inseriu na Etapa 2!

### 3. Integração com o Botpress (Avançado/Opcional)
Se o seu objetivo é escalar esse agente para as redes sociais (WhatsApp, Teams, Instagram), você pode usar o Botpress Cloud como intermediário das mensagens:
1. O Botpress Cloud não consegue acessar a porta `8000` do seu `localhost` diretamente pela internet.
2. Você precisará usar uma ferramenta de túnel (como o **ngrok**) para expor a sua máquina local para a nuvem temporariamente:
   ```bash
   ngrok http 8000
   ```
3. O Ngrok te dará um link público (ex: `https://meu-tunel.ngrok-free.app`). 
4. Vá até o painel do Botpress, crie um fluxo básico de chat e use o bloco de **"Execute Code"** ou **"API Call"** para disparar um `POST` para o endereço da nossa API (`https://meu-tunel.ngrok-free.app/chat`) contendo a pergunta do usuário no corpo JSON (`{"message": "sua pergunta", "user_id": "123"}`).
5. Capture a resposta do endpoint e retorne para o usuário final através de um bloco de "Text" na interface visual do Botpress.
