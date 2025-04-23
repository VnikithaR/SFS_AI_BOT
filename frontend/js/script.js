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
        chatbotContainer.style.display = chatbotContainer.style.display === 'none' ? 'flex' : 'none';
        chatbotBtn.classList.toggle('active');
    });


    chatbotBtn.addEventListener('click', () => {
        chatbotBtn.classList.toggle('active');
    });

    // Show confirmation popup when trying to close
    closeChatBtn.addEventListener('click', function () {
        confirmClosePopup.style.display = 'flex';
    });

    noBtn.addEventListener('click', function () {
        confirmClosePopup.style.display = 'none';
    });

    yesBtn.addEventListener('click', function () {
        chatbotContainer.style.display = 'none';
        confirmClosePopup.style.display = 'none';
    });

    popupClose.addEventListener('click', function () {
        confirmClosePopup.style.display = 'none';
    });

    // Settings modal toggle
    settingsIcon.addEventListener('click', function (e) {
        e.preventDefault();
        settingsModal.style.display = 'flex';
    });

    closeSettings.addEventListener('click', function () {
        settingsModal.style.display = 'none';
    });

    // Send message
    sendBtn.addEventListener('click', function () {
        const message = userInput.value.trim();
        if (message === '') return;

        appendMessage('user', message);
        userInput.value = '';
        typingIndicator.style.display = 'block';

        // ✅ Connect to Rasa
        fetch("http://localhost:5005/webhooks/rest/webhook", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                sender: "user",
                message: message
            })
        })
        .then(response => response.json())
        .then(data => {
            typingIndicator.style.display = 'none';

            if (data && data.length > 0) {
                data.forEach(botMsg => {
                    if (botMsg.text) {
                        appendMessage('bot', botMsg.text);
                    }
                });
            } else {
                appendMessage('bot', "Hmm... I didn't get a response. Try again?");
            }
        })
        .catch(error => {
            typingIndicator.style.display = 'none';
            appendMessage('bot', "Error connecting to Rasa server.");
            console.error("Fetch error:", error);
        });
    });

    userInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            sendBtn.click();
        }
    });

    // Append chat message
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

    // Clear chat window
    document.getElementById('refresh-btn').addEventListener('click', function () {
        chatWindow.innerHTML = '';
    });
});
