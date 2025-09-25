/* Chatbot Frontend JavaScript */
(function() {
    'use strict';

    let currentSessionId = null;
    let messageCount = 0;
    let totalTokens = 0;
    let isTyping = false;

    // DOM Elements
    const messageInput = document.getElementById('message-input');
    const sendBtn = document.getElementById('send-btn');
    const chatMessages = document.getElementById('chat-messages');
    const newChatBtn = document.getElementById('new-chat-btn');
    const sessionIdSpan = document.getElementById('session-id');
    const tokensUsedSpan = document.getElementById('tokens-used');
    const messageCountSpan = document.getElementById('message-count');
    const charCountSpan = document.getElementById('char-count');

    // Initialize
    document.addEventListener('DOMContentLoaded', function() {
        initializeChatbot();
        bindEvents();
    });

    function initializeChatbot() {
        // Create new session on load
        createNewSession();
        
        // Focus on input
        if (messageInput) {
            messageInput.focus();
        }
    }

    function bindEvents() {
        // Send button click
        if (sendBtn) {
            sendBtn.addEventListener('click', sendMessage);
        }

        // Enter key press
        if (messageInput) {
            messageInput.addEventListener('keypress', function(e) {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    sendMessage();
                }
            });

            // Character count
            messageInput.addEventListener('input', function() {
                const count = this.value.length;
                if (charCountSpan) {
                    charCountSpan.textContent = count;
                }
                
                // Change color if approaching limit
                if (count > 1800) {
                    charCountSpan.style.color = '#dc3545';
                } else if (count > 1500) {
                    charCountSpan.style.color = '#ffc107';
                } else {
                    charCountSpan.style.color = '#6c757d';
                }
            });
        }

        // New chat button
        if (newChatBtn) {
            newChatBtn.addEventListener('click', createNewSession);
        }
    }

    function createNewSession() {
        fetch('/chatbot/new_session', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({})
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                currentSessionId = data.session_id;
                updateSessionInfo();
                clearChat();
                showWelcomeMessage();
            } else {
                showError('Failed to create new session: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error creating session:', error);
            showError('Failed to create new session');
        });
    }

    function sendMessage() {
        const message = messageInput.value.trim();
        
        if (!message || isTyping) {
            return;
        }

        if (!currentSessionId) {
            showError('No active session. Please refresh the page.');
            return;
        }

        // Clear input and disable send button
        messageInput.value = '';
        updateCharCount();
        setSendButtonState(false);
        isTyping = true;

        // Add user message to chat
        addMessageToChat('user', message);

        // Show typing indicator
        showTypingIndicator();

        // Send to backend
        fetch('/chatbot/send_message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                session_id: currentSessionId
            })
        })
        .then(response => response.json())
        .then(data => {
            hideTypingIndicator();
            
            if (data.success) {
                // Add bot response
                addMessageToChat('bot', data.bot_response);
                
                // Update stats
                totalTokens += data.tokens_used || 0;
                updateStats();
                
                // Show token info
                if (data.tokens_used) {
                    showTokenInfo(data.tokens_used, data.response_time);
                }
            } else {
                addMessageToChat('bot', 'Sorry, I encountered an error: ' + data.error, true);
            }
        })
        .catch(error => {
            console.error('Error sending message:', error);
            hideTypingIndicator();
            addMessageToChat('bot', 'Sorry, there was a connection error. Please try again.', true);
        })
        .finally(() => {
            setSendButtonState(true);
            isTyping = false;
            messageInput.focus();
        });
    }

    function addMessageToChat(type, content, isError = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `${type}-message`;
        
        const now = new Date();
        const timeStr = now.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
        
        let avatarIcon = type === 'user' ? 'fa-user' : 'fa-robot';
        
        messageDiv.innerHTML = `
            <div class="message-avatar">
                <i class="fa ${avatarIcon}"></i>
            </div>
            <div class="message-content ${isError ? 'error-message' : ''}">
                <p>${escapeHtml(content)}</p>
                <small class="message-time">${timeStr}</small>
            </div>
        `;

        // Remove welcome message if it exists
        const welcomeMsg = chatMessages.querySelector('.welcome-message');
        if (welcomeMsg && type === 'user') {
            welcomeMsg.remove();
        }

        chatMessages.appendChild(messageDiv);
        scrollToBottom();
        
        // Update message count
        if (type === 'user') {
            messageCount++;
            updateStats();
        }
    }

    function showTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'bot-message typing-indicator';
        typingDiv.id = 'typing-indicator';
        
        typingDiv.innerHTML = `
            <div class="message-avatar">
                <i class="fa fa-robot"></i>
            </div>
            <div class="typing-dots">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        `;

        chatMessages.appendChild(typingDiv);
        scrollToBottom();
    }

    function hideTypingIndicator() {
        const typingIndicator = document.getElementById('typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }

    function showWelcomeMessage() {
        const welcomeDiv = document.createElement('div');
        welcomeDiv.className = 'welcome-message';
        
        welcomeDiv.innerHTML = `
            <div class="bot-message">
                <div class="message-avatar">
                    <i class="fa fa-robot"></i>
                </div>
                <div class="message-content">
                    <p>Hello! I'm your Gemini AI assistant. How can I help you today?</p>
                    <small class="message-time">Just now</small>
                </div>
            </div>
        `;

        chatMessages.appendChild(welcomeDiv);
        scrollToBottom();
    }

    function showTokenInfo(tokens, responseTime) {
        // You could add a small notification or update UI with token info
        console.log(`Tokens used: ${tokens}, Response time: ${responseTime}s`);
    }

    function clearChat() {
        chatMessages.innerHTML = '';
        messageCount = 0;
        totalTokens = 0;
        updateStats();
    }

    function updateSessionInfo() {
        if (sessionIdSpan) {
            sessionIdSpan.textContent = currentSessionId || '-';
        }
    }

    function updateStats() {
        if (tokensUsedSpan) {
            tokensUsedSpan.textContent = totalTokens;
        }
        if (messageCountSpan) {
            messageCountSpan.textContent = messageCount;
        }
    }

    function updateCharCount() {
        const count = messageInput ? messageInput.value.length : 0;
        if (charCountSpan) {
            charCountSpan.textContent = count;
        }
    }

    function setSendButtonState(enabled) {
        if (sendBtn) {
            sendBtn.disabled = !enabled;
            sendBtn.innerHTML = enabled ? 
                '<i class="fa fa-paper-plane"></i> Send' : 
                '<i class="fa fa-spinner fa-spin"></i> Sending...';
        }
    }

    function scrollToBottom() {
        if (chatMessages) {
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    }

    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    function showError(message) {
        console.error(message);
        // You could add a toast notification here
    }

})();