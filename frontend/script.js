const chatbotButton = document.querySelector('.chatbot-btn');
const chatbotContainer = document.querySelector('.chatbot-container');
const closeChatButton = document.querySelector('.close-chat');
const sendButton = document.querySelector('#send-btn');
const userInput = document.querySelector('#user-input');
const chatWindow = document.querySelector('#chat-window');
const refreshButton = document.querySelector('#refresh-btn');
const typingIndicator = document.querySelector('#typing-indicator');

// Toggle chatbot visibility
chatbotButton.addEventListener('click', () => {
    chatbotContainer.style.display = chatbotContainer.style.display === 'none' || chatbotContainer.style.display === '' ? 'flex' : 'none';
});

// Close chatbot when clicked
closeChatButton.addEventListener('click', () => {
    chatbotContainer.style.display = 'none';
});

// Function to get current time in 12-hour format
function getCurrentTime() {
    const now = new Date();
    let hours = now.getHours();
    let minutes = now.getMinutes();
    const ampm = hours >= 12 ? 'PM' : 'AM';
    hours = hours % 12;
    hours = hours ? hours : 12; // the hour '0' should be '12'
    minutes = minutes < 10 ? '0' + minutes : minutes;
    return hours + ':' + minutes + ' ' + ampm;
}

// Function to send a message
function sendMessage(message, sender) {
    const messageElement = document.createElement('div');
    const timestamp = document.createElement('span');
    messageElement.classList.add('chat-message', sender);
    
    // Create timestamp and append it to the message
    timestamp.classList.add('timestamp');
    timestamp.textContent = getCurrentTime();
    
    messageElement.textContent = message;
    messageElement.appendChild(timestamp);
    chatWindow.appendChild(messageElement);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

// Send message when clicking send button
sendButton.addEventListener('click', () => {
    const userMessage = userInput.value.trim();
    if (userMessage) {
        sendMessage(userMessage, 'user-message');
        userInput.value = '';
        typingIndicator.style.display = 'block'; // Show typing indicator
        setTimeout(() => {
            typingIndicator.style.display = 'none'; // Hide typing indicator after 2 seconds
            sendMessage('This is a bot response.', 'bot-message'); // Placeholder response
        }, 2000);
    }
});

// Send message when pressing Enter key
userInput.addEventListener('keypress', (event) => {
    if (event.key === 'Enter') {
        sendButton.click();
    }
});

// Refresh chat history
refreshButton.addEventListener('click', () => {
    chatWindow.innerHTML = '';
});
