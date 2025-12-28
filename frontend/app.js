const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const emojiBtn = document.getElementById('emoji-btn');
const emojiPicker = document.getElementById('emoji-picker');
const typingIndicator = document.getElementById('typing-indicator');
const quickReplies = document.getElementById('quick-replies');

let history = [];

// Format timestamp
function getTimestamp() {
    const now = new Date();
    const hours = now.getHours().toString().padStart(2, '0');
    const minutes = now.getMinutes().toString().padStart(2, '0');
    return `${hours}:${minutes}`;
}

// Add message to chat
function addMessage(content, role) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', role);

    const messageContent = document.createElement('div');
    messageContent.classList.add('message-content');

    const avatar = document.createElement('div');
    avatar.classList.add('avatar');
    avatar.textContent = role === 'user' ? '👤' : '🤖';

    const bubble = document.createElement('div');
    bubble.classList.add('bubble');

    const text = document.createElement('div');
    text.classList.add('text');

    // Preserve line breaks and formatting
    text.style.whiteSpace = 'pre-wrap';
    text.textContent = content;

    const timestamp = document.createElement('div');
    timestamp.classList.add('timestamp');
    timestamp.textContent = getTimestamp();

    bubble.appendChild(text);
    bubble.appendChild(timestamp);
    messageContent.appendChild(avatar);
    messageContent.appendChild(bubble);
    messageDiv.appendChild(messageContent);

    // Insert before typing indicator or at the end
    const typingDiv = document.getElementById('typing-indicator');
    if (typingDiv && typingDiv.parentNode === chatMessages) {
        chatMessages.insertBefore(messageDiv, typingDiv);
    } else {
        chatMessages.appendChild(messageDiv);
    }

    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Show typing indicator
function showTyping() {
    typingIndicator.style.display = 'block';
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Hide typing indicator
function hideTyping() {
    typingIndicator.style.display = 'none';
}

// Send message
async function sendMessage(text = null) {
    const messageText = text || userInput.value.trim();
    if (!messageText) return;

    addMessage(messageText, 'user');
    userInput.value = '';


    // Add to history
    history.push({ role: "user", content: messageText });

    // Show typing indicator
    showTyping();

    try {
        const response = await fetch('http://localhost:8000/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ history: history })
        });

        hideTyping();

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        const botResponse = data.response;

        addMessage(botResponse, 'bot');
        history.push({ role: "assistant", content: botResponse });

    } catch (error) {
        hideTyping();
        console.error('Error:', error);
        addMessage("Sorry, I'm having trouble connecting to the server. Please try again.", 'bot');
    }
}

// Emoji picker toggle
emojiBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    emojiPicker.style.display = emojiPicker.style.display === 'none' ? 'block' : 'none';
});

// Close emoji picker when clicking outside
document.addEventListener('click', (e) => {
    if (!emojiPicker.contains(e.target) && e.target !== emojiBtn) {
        emojiPicker.style.display = 'none';
    }
});

// Emoji selection
document.querySelectorAll('.emoji-item').forEach(emoji => {
    emoji.addEventListener('click', () => {
        userInput.value += emoji.textContent;
        userInput.focus();
        emojiPicker.style.display = 'none';
    });
});

// Quick reply buttons
document.querySelectorAll('.quick-reply-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const text = btn.getAttribute('data-text');
        sendMessage(text);
    });
});

// Send button click
sendBtn.addEventListener('click', () => sendMessage());

// Enter key to send
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

// Focus input on load
userInput.focus();
