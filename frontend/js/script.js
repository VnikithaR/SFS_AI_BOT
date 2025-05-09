document.addEventListener('DOMContentLoaded', function () {
  // -------- Elements --------
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
  const navOverlay = document.getElementById('nav-overlay');

  const loginBtn = document.querySelector('#login-link'); 
  const loginOverlay = document.querySelector('.overlay');
  const loginWrapper = document.querySelector('.auth-wrapper.login-form');

  // -------- Navigation Menu Toggle --------
  menuToggle.addEventListener('change', function () {
    toggleMenu(this.checked);
  });

  navOverlay.addEventListener('click', function () {
    toggleMenu(false);
  });

  function toggleMenu(show) {
    if (show) {
      menu.classList.add('open');
      navOverlay.classList.add('show');
    } else {
      menu.classList.remove('open');
      navOverlay.classList.remove('show');
      menuToggle.checked = false;
    }
  }

  // -------- Chatbot Logic --------
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
sendBtn.addEventListener('click', async () => {
  const message = userInput.value.trim();
  if (!message) return;

  appendMessage('user', message);
  userInput.value = '';
  typingIndicator.style.display = 'block';

  const response = await fetch("http://localhost:5005/webhooks/rest/webhook", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      sender: "user",  // could be dynamic for each session
      message: message
    })
  });

  const data = await response.json();
  typingIndicator.style.display = 'none';

  data.forEach(botMsg => {
    appendMessage('bot', botMsg.text);
  });
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

  // -------- Login Modal --------
  if (loginBtn && loginOverlay && loginWrapper) {
    loginBtn.addEventListener('click', function (e) {
      e.preventDefault();
      document.body.classList.add('login-active');
      loginOverlay.style.display = 'block';
      loginWrapper.style.display = 'block';
    });

    loginOverlay.addEventListener('click', function () {
      document.body.classList.remove('login-active');
      loginOverlay.style.display = 'none';
      loginWrapper.style.display = 'none';
    });
  }

  // -------- Show User Features Function --------
  window.showUserFeatures = function (user) {
    document.getElementById("login-link").style.display = "none";
    document.getElementById("logout-link").style.display = "inline";
    document.getElementById("profile-link").style.display = "inline";
    document.getElementById("settings-link").style.display = "inline";


    document.getElementById("user-welcome-message").style.display = "block";
    document.getElementById("user-name").innerText = user.name;


    document.getElementById("profile-name").innerText = user.name;
    document.getElementById("profile-email").innerText = user.email;
    document.getElementById("profile-course").innerText = user.course || "N/A";


    document.getElementById("support-name").value = user.name;
    document.getElementById("support-email").value = user.email;


    document.getElementById("dashboard-section").style.display = "block";
    document.getElementById("profile-section").style.display = "block";
    document.getElementById("application-status").style.display = "block";
    document.getElementById("academic-info").style.display = "block";
    document.getElementById("support-section").style.display = "block";
  };


  // -------- Logout Function --------
  window.logout = function () {
    localStorage.clear(); // or clear cookies
    location.href = "/";  // redirect to homepage
  };


  // -------- Navigation Scroll Hooks --------
  const profileLink = document.getElementById("profile-link");
  if (profileLink) {
    profileLink.addEventListener("click", function (e) {
      e.preventDefault();
      const section = document.getElementById("profile-section");
      if (section) section.scrollIntoView({ behavior: "smooth" });
    });
  }


  const settingsLink = document.getElementById("settings-link");
  if (settingsLink) {
    settingsLink.addEventListener("click", function (e) {
      e.preventDefault();
      settingsModal.style.display = "flex";
    });
  }

  // -------- Logout Function Placeholder --------
  window.logout = function () {
    alert("Logged out!"); // Replace with actual logic
  };
});
