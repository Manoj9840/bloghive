class BlogHiveChatbot {
    constructor() {
        this.apiUrl = 'http://127.0.0.1:8000/api/chatbot/';
        this.isOpen = false;
        this.init();
    }

    init() {
        this.injectHTML();
        this.cacheDOM();
        this.bindEvents();
        this.addPulse();
        this.showQuickReplies();
    }

    injectHTML() {
        const chatbotHTML = `
            <div id="bh-chatbot-widget" class="bh-chatbot-widget">
                <button id="bh-chatbot-toggle" class="bh-chatbot-toggle" aria-label="Open Chat">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                    </svg>
                </button>
                <div id="bh-chatbot-window" class="bh-chatbot-window">
                    <div class="bh-chatbot-header">
                        <div class="bh-chatbot-title">
                            <span class="status-dot"></span>
                            BlogHive AI Assistant
                        </div>
                        <button id="bh-chatbot-close" class="bh-chatbot-close">&times;</button>
                    </div>
                    <div id="bh-chatbot-messages" class="bh-chatbot-messages">
                        <div class="message bot">
                            Hello! I'm your BlogHive assistant. How can I help you today?
                        </div>
                    </div>
                    <form id="bh-chatbot-form" class="bh-chatbot-input-area">
                        <input type="text" id="bh-chatbot-input" placeholder="Type your question..." autocomplete="off" required>
                        <button type="submit" class="bh-chatbot-send" id="bh-chatbot-send-btn">
                            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                <line x1="22" y1="2" x2="11" y2="13"></line>
                                <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
                            </svg>
                        </button>
                    </form>
                </div>
            </div>
        `;
        document.body.insertAdjacentHTML('beforeend', chatbotHTML);
    }

    cacheDOM() {
        this.widget = document.getElementById('bh-chatbot-widget');
        this.toggleBtn = document.getElementById('bh-chatbot-toggle');
        this.closeBtn = document.getElementById('bh-chatbot-close');
        this.chatWindow = document.getElementById('bh-chatbot-window');
        this.messagesContainer = document.getElementById('bh-chatbot-messages');
        this.form = document.getElementById('bh-chatbot-form');
        this.input = document.getElementById('bh-chatbot-input');
        this.sendBtn = document.getElementById('bh-chatbot-send-btn');
    }

    bindEvents() {
        this.toggleBtn.addEventListener('click', () => this.toggleChat());
        this.closeBtn.addEventListener('click', () => this.toggleChat(false));
        this.form.addEventListener('submit', (e) => this.handleSubmit(e));
    }

    toggleChat(forceState) {
        this.isOpen = forceState !== undefined ? forceState : !this.isOpen;
        if (this.isOpen) {
            this.chatWindow.classList.add('active');
            this.toggleBtn.classList.add('hidden');
            this.toggleBtn.classList.remove('pulse'); // Stop pulsing when opened
            this.input.focus();
        } else {
            this.chatWindow.classList.remove('active');
            this.toggleBtn.classList.remove('hidden');
        }
    }

    addPulse() {
        this.toggleBtn.classList.add('pulse');
    }

    showQuickReplies() {
        const replies = [
            "How do I create a blog?",
            "What Categories are there?",
            "How does the AI work?",
            "Can I edit my posts?"
        ];

        const container = document.createElement('div');
        container.className = 'bh-chatbot-quick-replies';
        
        replies.forEach(text => {
            const btn = document.createElement('button');
            btn.className = 'quick-reply-btn';
            btn.textContent = text;
            btn.onclick = () => this.sendMessage(text);
            container.appendChild(btn);
        });

        this.messagesContainer.appendChild(container);
        this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
    }

    addMessage(text, sender) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${sender}`;
        msgDiv.textContent = text;
        this.messagesContainer.appendChild(msgDiv);
        this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
    }

    showTyping() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message bot typing';
        typingDiv.id = 'bh-typing-indicator';
        typingDiv.innerHTML = '<span></span><span></span><span></span>';
        this.messagesContainer.appendChild(typingDiv);
        this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
    }

    hideTyping() {
        const typingDiv = document.getElementById('bh-typing-indicator');
        if (typingDiv) typingDiv.remove();
    }

    async handleSubmit(e) {
        e.preventDefault();
        const query = this.input.value.trim();
        if (!query) return;
        this.sendMessage(query);
        this.input.value = '';
    }

    async sendMessage(query) {
        // Add user message
        this.addMessage(query, 'user');
        
        this.input.disabled = true;
        this.sendBtn.disabled = true;

        this.showTyping();

        try {
            const response = await fetch(this.apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ query: query })
            });

            const data = await response.json();
            this.hideTyping();
            
            if (response.ok) {
                this.addMessage(data.answer, 'bot');
            } else {
                this.addMessage("I'm sorry, I encountered an error. Please try again later.", 'bot');
            }
        } catch (error) {
            console.error('Chatbot error:', error);
            this.hideTyping();
            this.addMessage("I'm having trouble connecting right now. Please check your connection.", 'bot');
        } finally {
            this.input.disabled = false;
            this.sendBtn.disabled = false;
            if (this.isOpen) this.input.focus();
        }
    }
}

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', () => {
    window.blogHiveChatbot = new BlogHiveChatbot();
});
