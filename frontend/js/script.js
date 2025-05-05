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

  // Initially hide the chatbot container on page load
  chatbotContainer.style.display = 'none';

  // Slide carousel
  let slideIndex = 0;
  const slides = document.querySelectorAll('.carousel img');
  setInterval(() => {
    slides.forEach(slide => slide.classList.remove('active'));
    slideIndex = (slideIndex + 1) % slides.length;
    slides[slideIndex].classList.add('active');
  }, 4000);

  // Show/hide chatbot
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

  // Confirm chat close
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

  // Settings modal
  settingsIcon.addEventListener('click', (e) => {
    e.preventDefault();
    settingsModal.style.display = 'flex';
  });

  closeSettings.addEventListener('click', () => {
    settingsModal.style.display = 'none';
  });

  // Chatbot send
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

  // -------- Login / Signup / Reset Logic (Frontend Only) --------
  const loginForm = document.getElementById("login-form");
  const signupForm = document.getElementById("signup-form");
  const forgotPasswordLink = document.getElementById("forgot-password");
  const forgotPasswordModal = document.getElementById("forgot-password-modal");
  const closeModalBtn = document.getElementById("close-modal");
  const resetPasswordForm = document.getElementById("reset-password-form");

  // Toggle between Login and Signup
  function toggleAuthTabs() {
    if (document.getElementById("tab-login").checked) {
      loginForm.style.display = "block";
      signupForm.style.display = "none";
    } else if (document.getElementById("tab-signup").checked) {
      loginForm.style.display = "none";
      signupForm.style.display = "block";
    }
  }

  toggleAuthTabs(); // Run once on load

  document.getElementById("tab-login").addEventListener("change", toggleAuthTabs);
  document.getElementById("tab-signup").addEventListener("change", toggleAuthTabs);

  // Simulate database with localStorage
  let users = JSON.parse(localStorage.getItem('users')) || [];

  loginForm.addEventListener('submit', function (e) {
    e.preventDefault();
    const email = this.querySelector('input[type="email"]').value.trim();
    const password = this.querySelector('input[type="password"]').value.trim();

    const user = users.find(u => u.email === email && u.password === password);
    if (user) {
      alert("Login successful!");
      window.location.href = "dashboard.html"; // or simulate login
    } else {
      alert("Invalid email or password.");
    }
  });

  signupForm.addEventListener('submit', function (e) {
    e.preventDefault();
    const fullName = this.querySelector('input[placeholder="Full Name"]').value.trim();
    const email = this.querySelectorAll('input[type="email"]')[1].value.trim();
    const password = this.querySelectorAll('input[type="password"]')[0].value.trim();
    const confirmPassword = this.querySelectorAll('input[type="password"]')[1].value.trim();

    if (password !== confirmPassword) {
      alert("Passwords do not match.");
      return;
    }

    if (users.find(u => u.email === email)) {
      alert("User already exists.");
      return;
    }

    users.push({ fullName, email, password });
    localStorage.setItem('users', JSON.stringify(users));
    alert("Signup successful!");
    window.location.href = "dashboard.html"; // or simulate login
  });

  resetPasswordForm.addEventListener('submit', function (e) {
    e.preventDefault();
    const email = document.getElementById('reset-email').value.trim();
    const newPassword = document.getElementById('new-password').value.trim();

    const userIndex = users.findIndex(u => u.email === email);
    if (userIndex === -1) {
      alert("No user found with that email.");
      return;
    }

    users[userIndex].password = newPassword;
    localStorage.setItem('users', JSON.stringify(users));
    alert("Password reset successful.");
    forgotPasswordModal.classList.add('hidden');
  });

  // Show the login popup
  document.querySelector('.login-btn').addEventListener('click', function (e) {
    e.preventDefault();
    document.body.classList.add('login-active');
  });

  // Close modal on successful login or cancel
  document.getElementById('login-form').addEventListener('submit', function (e) {
    e.preventDefault(); // Remove this if you want actual form submit
    document.body.classList.remove('login-active');
  });

  // Optional: Close if clicking outside (overlay)
  document.querySelector('.overlay').addEventListener('click', function () {
    document.body.classList.remove('login-active');
  });

  // Toggle login overlay
  document.querySelector('.login-btn').addEventListener('click', function (e) {
    e.preventDefault();
    document.getElementById('login-overlay').querySelector('.overlay').classList.add('show');
    document.getElementById('login-overlay').querySelector('.auth-wrapper').classList.add('show');
  });

  // Close overlay on background click
  document.querySelector('#login-overlay .overlay').addEventListener('click', function () {
    this.classList.remove('show');
    document.getElementById('login-overlay').querySelector('.auth-wrapper').classList.remove('show');
  });
});
