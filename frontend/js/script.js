document.addEventListener('DOMContentLoaded', function () {
  // -------- Chatbot Elements --------
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
  const refreshBtn = document.getElementById('refresh-btn');
  const menuToggle = document.getElementById('menu-toggle');
  const menu = document.getElementById('menu');

  menuToggle.addEventListener('change', () => {
    menu.classList.toggle('open');
  });

  function logout() {
    alert("Logged out!"); // Replace with actual logic
  }

  // -------- Chatbot Behavior --------
  chatbotContainer.style.display = 'none';
  let welcomeMessageShown = false;

  chatbotBtn.addEventListener('click', () => {
    const isVisible = chatbotContainer.style.display !== 'none';
    chatbotContainer.style.display = isVisible ? 'none' : 'flex';
    chatbotBtn.classList.toggle('active');

    if (!isVisible && !welcomeMessageShown) {
      appendMessage('bot', "Hi there! 👋 I'm SFS InfoBot. How can I assist you today?");
      welcomeMessageShown = true;
    }
  });

  closeChatBtn.addEventListener('click', () => {
    confirmClosePopup.style.display = 'flex';
  });

  noBtn.addEventListener('click', () => {
    confirmClosePopup.style.display = 'none';
  });

  yesBtn.addEventListener('click', () => {
    chatbotContainer.style.display = 'none';
    confirmClosePopup.style.display = 'none';
  });

  popupClose.addEventListener('click', () => {
    confirmClosePopup.style.display = 'none';
  });

  settingsIcon.addEventListener('click', (e) => {
    e.preventDefault();
    settingsModal.style.display = 'flex';
  });

  closeSettings.addEventListener('click', () => {
    settingsModal.style.display = 'none';
  });

  // -------- Chat Send Message --------
  sendBtn.addEventListener('click', () => {
    const message = userInput.value.trim();
    if (!message) return;

    appendMessage('user', message);
    userInput.value = '';
    typingIndicator.style.display = 'block';

    setTimeout(() => {
      typingIndicator.style.display = 'none';
      appendMessage('bot', "🤖 I'm just a demo bot! Your message was: " + message);
    }, 1000);
  });

  userInput.addEventListener('keypress', function (e) {
    if (e.key === 'Enter') sendBtn.click();
  });

  refreshBtn.addEventListener('click', () => {
    chatWindow.innerHTML = '';
  });

  function appendMessage(sender, text) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('chat-message', sender === 'user' ? 'user-message' : 'bot-message');
    messageDiv.textContent = text;

    const timestamp = document.createElement('div');
    timestamp.classList.add('timestamp');
    timestamp.textContent = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    messageDiv.appendChild(timestamp);
    chatWindow.appendChild(messageDiv);
    chatWindow.scrollTop = chatWindow.scrollHeight;
  }

  // -------- Carousel (Optional) --------
  let slideIndex = 0;
  const slides = document.querySelectorAll('.carousel img');
  if (slides.length > 0) {
    slides[slideIndex].classList.add('active');
    setInterval(() => {
      slides.forEach(slide => slide.classList.remove('active'));
      slideIndex = (slideIndex + 1) % slides.length;
      slides[slideIndex].classList.add('active');
    }, 4000);
  }

  // -------- Login UI Modal Trigger Only --------
  const loginBtn = document.querySelector('.login-btn');
  const overlay = document.querySelector('.overlay');
  const loginWrapper = document.querySelector('.auth-wrapper.login-form');

  if (loginBtn && overlay && loginWrapper) {
    loginBtn.addEventListener('click', function (e) {
      e.preventDefault();
      document.body.classList.add('login-active');
      overlay.style.display = 'block';
      loginWrapper.style.display = 'block';
    });

    overlay.addEventListener('click', function () {
      document.body.classList.remove('login-active');
      overlay.style.display = 'none';
      loginWrapper.style.display = 'none';
    });
  }
});