document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const messageInput = document.getElementById('message-input');
    const chatMessages = document.getElementById('chat-messages');
    const sendBtn = document.getElementById('send-btn');
    const clearBtn = document.getElementById('clear-btn');

    // Inicialização do usuário fictício
    const userId = "browser_user_" + Math.floor(Math.random() * 10000);

    // Carregar histórico
    let history = JSON.parse(localStorage.getItem('chat_history')) || [];
    
    if (history.length === 0) {
        // Mensagem inicial de boas-vindas se não houver histórico
        addMessageToUI('bot', 'Olá! Sou o assistente virtual da Seguros Cloud IO. Como posso ajudar você hoje?');
    } else {
        // Renderizar histórico
        history.forEach(msg => addMessageToUI(msg.role, msg.content, false));
        scrollToBottom();
    }

    // Limpar histórico
    clearBtn.addEventListener('click', () => {
        if(confirm("Tem certeza que deseja limpar o histórico desta conversa?")) {
            localStorage.removeItem('chat_history');
            chatMessages.innerHTML = '';
            history = [];
            addMessageToUI('bot', 'Histórico limpo. Como posso ajudar agora?');
        }
    });

    // Submissão do formulário
    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const message = messageInput.value.trim();
        if (!message) return;

        // 1. Adicionar mensagem do usuário
        addMessageToUI('user', message);
        saveToHistory('user', message);
        messageInput.value = '';
        messageInput.focus();
        
        // 2. Mostrar indicador de "Digitando..."
        const typingId = showTypingIndicator();
        sendBtn.disabled = true;

        try {
            // 3. Fazer requisição à API Real
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    user_id: userId,
                    message: message
                })
            });

            if (!response.ok) {
                throw new Error('Erro na comunicação com o servidor.');
            }

            const data = await response.json();
            
            // 4. Remover indicador e mostrar resposta do bot
            removeElement(typingId);
            addMessageToUI('bot', data.response);
            saveToHistory('bot', data.response);

        } catch (error) {
            console.error('Erro:', error);
            removeElement(typingId);
            addMessageToUI('bot', 'Desculpe, ocorreu um erro de conexão. Tente novamente mais tarde.');
        } finally {
            sendBtn.disabled = false;
        }
    });

    function addMessageToUI(role, text, animate = true) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${role}-message`;
        
        // Formatação simples para quebra de linhas e negrito do LLM
        const formattedText = text
            .replace(/\n/g, '<br>')
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

        const time = new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});

        msgDiv.innerHTML = `
            <div class="message-content">${formattedText}</div>
            <div class="message-time">${time}</div>
        `;

        if (!animate) {
            msgDiv.style.animation = 'none';
        }

        chatMessages.appendChild(msgDiv);
        scrollToBottom();
    }

    function saveToHistory(role, content) {
        history.push({ role, content });
        // Manter apenas as últimas 50 mensagens para não pesar o storage
        if (history.length > 50) history.shift();
        localStorage.setItem('chat_history', JSON.stringify(history));
    }

    function showTypingIndicator() {
        const id = 'typing-' + Date.now();
        const msgDiv = document.createElement('div');
        msgDiv.className = `message bot-message`;
        msgDiv.id = id;
        
        msgDiv.innerHTML = `
            <div class="message-content typing-indicator">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        `;
        
        chatMessages.appendChild(msgDiv);
        scrollToBottom();
        return id;
    }

    function removeElement(id) {
        const el = document.getElementById(id);
        if (el) el.remove();
    }

    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
});
