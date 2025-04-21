document.addEventListener('DOMContentLoaded', function () {
    const chatbotBtn = document.getElementById('chatbot-btn');
    const chatbotContainer = document.getElementById('chatbot-container');
    const closeChatBtn = document.getElementById('close-chat');
    const confirmClosePopup = document.getElementById('confirm-close-popup');
    const popupClose = document.getElementById('popup-close');
    const yesBtn = document.getElementById('yes-btn');
    const noBtn = document.getElementById('no-btn');
    const settingsIcon = document.getElementById('settings-icon');
    const settingsModal = document.getElementById('settings-modal');
    const closeSettings = document.getElementById('close-settings');
    const sendBtn = document.getElementById('send-btn');
    const userInput = document.getElementById('user-input');
    const chatWindow = document.getElementById('chat-window');
    const typingIndicator = document.getElementById('typing-indicator');

    // Initially hide the chatbot container
    chatbotContainer.style.display = 'none';

    // College website UI (Carousel)
    let slideIndex = 0;
    const slides = document.querySelectorAll('.carousel img');

    function showSlides() {
        slides.forEach((slide) => {
            slide.classList.remove('active');
        });
        slideIndex = (slideIndex + 1) % slides.length;
        slides[slideIndex].classList.add('active');
    }

    setInterval(showSlides, 4000);

    // Toggle chatbot visibility
    chatbotBtn.addEventListener('click', function () {
        if (chatbotContainer.style.display === 'none' || chatbotContainer.style.display === '') {
            chatbotContainer.style.display = 'flex'; // Show the chatbot
        } else {
            chatbotContainer.style.display = 'none'; // Hide the chatbot
        }
    });
    chatbotBtn.addEventListener('click', () => {
        chatbotBtn.classList.toggle('active');
    });

    // Show confirmation popup when trying to close
    closeChatBtn.addEventListener('click', function () {
        confirmClosePopup.style.display = 'flex';
    });

    // Cancel closing
    noBtn.addEventListener('click', function () {
        confirmClosePopup.style.display = 'none';
    });

    // Confirm closing
    yesBtn.addEventListener('click', function () {
        chatbotContainer.style.display = 'none';
        confirmClosePopup.style.display = 'none';
    });

    // Popup close button
    popupClose.addEventListener('click', function () {
        confirmClosePopup.style.display = 'none';
    });

    // Settings icon opens modal
    settingsIcon.addEventListener('click', function (e) {
        e.preventDefault();
        settingsModal.style.display = 'flex';
    });

    // Close settings modal
    closeSettings.addEventListener('click', function () {
        settingsModal.style.display = 'none';
    });

    // Send message and simulate bot response
    sendBtn.addEventListener('click', function () {
        const message = userInput.value.trim();
        if (message === '') return;

        appendMessage('user', message);
        userInput.value = '';

        // Simulate bot typing
        typingIndicator.style.display = 'block';

        setTimeout(() => {
            typingIndicator.style.display = 'none';
            appendMessage('bot', generateBotResponse(message));
        }, 1000);
    });

    // Press Enter to send message
    userInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            sendBtn.click();
        }
    });

    // Append message to chat
    function appendMessage(sender, text) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('chat-message', sender === 'user' ? 'user-message' : 'bot-message');
        messageDiv.textContent = text;

        const timestamp = document.createElement('div');
        timestamp.classList.add('timestamp');
        const now = new Date();
        timestamp.textContent = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

        messageDiv.appendChild(timestamp);
        chatWindow.appendChild(messageDiv);
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }

    // Generate simple bot response
    function generateBotResponse(userMessage) {
        const responses = {
            hello: "Hi! How can I help you with admissions or courses today?",
            hi: "Hello! 😊 What would you like to know?",
            admissions: "Admissions are open! Visit the Admissions section for more info.",
            courses: "We offer various UG & PG programs. Check out the Courses section.",
            default: "I'm here to help! Ask me about the college, admissions, courses, and more."
        };

        const lower = userMessage.toLowerCase();
        for (let key in responses) {
            if (lower.includes(key)) return responses[key];
        }

        return responses.default;
    }

    // Refresh button to clear chat
    document.getElementById('refresh-btn').addEventListener('click', function () {
        chatWindow.innerHTML = '';
    });
});
