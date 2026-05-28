# Planejamento: Documentação do Sistema para Leigos

## Overview
O objetivo deste projeto é gerar um documento detalhado, claro e didático (`docs/arquitetura_e_uso.md`), explicando toda a estrutura do sistema Seguros Cloud IO. O foco é permitir que pessoas não técnicas (leigos, gestores, clientes) compreendam o fluxo de ponta a ponta: desde a interface web até o processamento da inteligência artificial. O documento incluirá diagramas visuais e um manual de "Como Usar".

## Project Type
WEB / Documentação

## Success Criteria
- [ ] O documento explica a arquitetura sem jargões complexos (ou explicando-os com analogias).
- [ ] O documento contém ao menos um diagrama visual (Mermaid) mostrando o fluxo da informação.
- [ ] O documento possui uma seção clara e passo-a-passo de como o usuário final deve interagir com o chat.
- [ ] A documentação está formatada em Markdown legível e atraente.

## Tech Stack
- **Markdown:** Para a estruturação do texto.
- **Mermaid JS:** Para renderização de diagramas visuais e fluxogramas diretamente no GitHub/Markdown.

## File Structure
- `docs/PLAN-system-docs.md` (Este arquivo)
- `docs/arquitetura_e_uso.md` (Arquivo final a ser gerado)

## Task Breakdown

### Tarefa 1: Criação da Estrutura e Diagrama Principal
- **Agente:** `technical-writer` / `orchestrator`
- **Ação:** Criar o arquivo `docs/arquitetura_e_uso.md`. Escrever a introdução (O que é o sistema?) e criar o diagrama Mermaid mostrando as três camadas: Interface do Usuário (Chat) -> Cérebro do Sistema (API) -> Base de Conhecimento (IA/Ollama).
- **INPUT:** Plano aprovado.
- **OUTPUT:** Arquivo criado com introdução e diagrama.
- **VERIFY:** Diagrama Mermaid renderiza corretamente sem erros de sintaxe.

### Tarefa 2: Explicação Didática dos Componentes
- **Agente:** `technical-writer`
- **Ação:** Adicionar as seções explicando cada componente (O que é a Interface Web, o que é o RAG/Memória, e o que é o Ollama/LLM) utilizando analogias do dia a dia (ex: o Ollama é o cérebro que pensa, o ChromaDB é o livro de regras que ele consulta).
- **INPUT:** Estrutura da Tarefa 1.
- **OUTPUT:** Seções descritivas finalizadas.
- **VERIFY:** O texto está livre de termos excessivamente técnicos sem explicação.

### Tarefa 3: Guia de Uso (Como Usar)
- **Agente:** `technical-writer`
- **Ação:** Adicionar a seção final mostrando um passo-a-passo para o usuário leigo: como abrir o chat, como formular boas perguntas para a IA, e o que fazer se a IA não souber a resposta (handoff humano).
- **INPUT:** Documento com a arquitetura finalizada.
- **OUTPUT:** Documento completo e pronto.
- **VERIFY:** Instruções estão claras e condizem com o comportamento real do bot.

## Phase X: Verification
- [ ] **Lint Markdown:** O arquivo markdown não possui erros de formatação.
- [ ] **Validação Visual:** Os blocos de código e diagramas Mermaid estão corretos.
- [ ] **UX/Didática:** O Socratic Gate foi respeitado e o escopo solicitado pelo usuário foi cumprido à risca.

---
**Status:** Aguardando Aprovação do Usuário para iniciar a implementação.
