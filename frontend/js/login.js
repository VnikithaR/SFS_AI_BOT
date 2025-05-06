document.addEventListener('DOMContentLoaded', function () {
    const API_BASE = "http://localhost:5000"; // Flask backend

    // DOM Elements
    const loginForm = document.getElementById("login-form");
    const signupForm = document.getElementById("signup-form");
    const forgotPasswordLink = document.querySelector(".forgot-password-link");
    const forgotPasswordModal = document.getElementById("forgot-password-modal");
    const closeModalBtn = document.getElementById("close-modal");
    const resetPasswordForm = document.getElementById("reset-password-form");
    const loginBtn = document.querySelector(".login-btn");
    const overlay = document.querySelector(".overlay");
    const loginWrapper = document.querySelector(".auth-wrapper.login-form");

    const loginTab = document.getElementById("tab-login");
    const signupTab = document.getElementById("tab-signup");

    const passwordToggleLogin = document.getElementById("password-toggle-login");
    const passwordToggleSignup = document.getElementById("password-toggle-signup");
    const passwordLogin = loginForm.querySelector('input[type="password"]');
    const passwordSignup = signupForm.querySelectorAll('input[type="password"]')[0];
    const confirmPasswordSignup = signupForm.querySelectorAll('input[type="password"]')[1];

    const loginLink = document.querySelector(".login-link");
    const signUpLink = document.querySelector(".sign-up-link");

    // === Helper Functions ===
    function validateEmail(email) {
        const emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
        return emailPattern.test(email);
    }

    function toggleAuthTabs() {
        loginForm.style.display = loginTab.checked ? "block" : "none";
        signupForm.style.display = signupTab.checked ? "block" : "none";
    }

    function closeModal() {
        document.body.classList.remove("login-active", "forgot-password-active");
        overlay.style.display = "none";
        loginWrapper.style.display = "none";
        forgotPasswordModal.style.display = "none";
    }

    // === Modal and Tab Controls ===
    loginBtn.addEventListener("click", function (e) {
        e.preventDefault();
        document.body.classList.remove("forgot-password-active");
        forgotPasswordModal.style.display = "none";
        document.body.classList.add("login-active");
        overlay.style.display = "block";
        loginWrapper.style.display = "block";
        toggleAuthTabs();
    });

    overlay.addEventListener("click", closeModal);
    closeModalBtn.addEventListener("click", closeModal);

    loginTab.addEventListener("change", toggleAuthTabs);
    signupTab.addEventListener("change", toggleAuthTabs);

    forgotPasswordLink.addEventListener("click", function (e) {
        e.preventDefault();
        document.body.classList.remove("login-active");
        loginWrapper.style.display = "none";
        document.body.classList.add("forgot-password-active");
        forgotPasswordModal.style.display = "block";
        overlay.style.display = "block";
    });

    if (loginLink) {
        loginLink.addEventListener("click", function (e) {
            e.preventDefault();
            loginTab.checked = true;
            toggleAuthTabs();
        });
    }

    if (signUpLink) {
        signUpLink.addEventListener("click", function (e) {
            e.preventDefault();
            signupTab.checked = true;
            toggleAuthTabs();
        });
    }

    // === Password Visibility Toggles ===
    if (passwordToggleLogin) {
        passwordToggleLogin.addEventListener("click", function () {
            passwordLogin.type = passwordLogin.type === "password" ? "text" : "password";
            this.classList.toggle("show-password");
        });
    }

    if (passwordToggleSignup) {
        passwordToggleSignup.addEventListener("click", function () {
            const isHidden = passwordSignup.type === "password";
            passwordSignup.type = isHidden ? "text" : "password";
            confirmPasswordSignup.type = isHidden ? "text" : "password";
            this.classList.toggle("show-password");
        });
    }

    // === Signup Handler ===
    signupForm.addEventListener("submit", async function (e) {
        e.preventDefault();
        const fullName = this.querySelector('input[placeholder="Full Name"]').value.trim();
        const email = this.querySelector('input[type="email"]').value.trim();
        const password = passwordSignup.value.trim();
        const confirmPassword = confirmPasswordSignup.value.trim();

        if (!fullName || !email || !password || !confirmPassword) {
            alert("Please fill out all fields.");
            return;
        }

        if (!validateEmail(email)) {
            alert("Please enter a valid email.");
            return;
        }

        if (password !== confirmPassword) {
            alert("Passwords do not match.");
            return;
        }

        try {
            const res = await fetch(`${API_BASE}/signup`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ fullName, email, password })
            });
            const data = await res.json();
            alert(data.message);
            if (data.success) {
                loginTab.checked = true;
                toggleAuthTabs();
            }
        } catch (err) {
            console.error(err);
            alert("Signup failed. Please try again.");
        }
    });

    // === Login Handler ===
    loginForm.addEventListener("submit", async function (e) {
        e.preventDefault();
        const email = this.querySelector('input[type="email"]').value.trim();
        const password = passwordLogin.value.trim();

        if (!email || !password) {
            alert("Please enter both email and password.");
            return;
        }

        try {
            const res = await fetch(`${API_BASE}/login`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, password })
            });
            const data = await res.json();
            alert(data.message);
            if (data.success) {
                closeModal();
                // Redirect or store session info here if needed
            }
        } catch (err) {
            console.error(err);
            alert("Login failed. Please try again.");
        }
    });

    // === Reset Password Handler ===
    resetPasswordForm.addEventListener("submit", async function (e) {
        e.preventDefault();
        const email = this.querySelector('input[type="email"]').value.trim();

        if (!validateEmail(email)) {
            alert("Please enter a valid email.");
            return;
        }

        const newPassword = prompt("Enter your new password:");
        if (!newPassword) return;

        try {
            const res = await fetch(`${API_BASE}/reset-password`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, newPassword })
            });
            const data = await res.json();
            alert(data.message);
            if (data.success) closeModal();
        } catch (err) {
            console.error(err);
            alert("Password reset failed. Please try again.");
        }
    });
    // Initial setup
    toggleAuthTabs();
});


// Simulated authentication state
let isAuthenticated = false;
let currentUser = { name: "" };

// Call this function after login
function login(userName) {
  isAuthenticated = true;
  currentUser.name = userName;
  updateNavForAuth();
}

// Call this function on logout
function logout() {
  isAuthenticated = false;
  currentUser.name = "";
  updateNavForAuth();
  alert("You have been logged out.");
}

// Show/hide links based on authentication
function updateNavForAuth() {
  document.getElementById("login-link").style.display = isAuthenticated ? "none" : "inline";
  document.getElementById("profile-link").style.display = isAuthenticated ? "inline" : "none";
  document.getElementById("settings-link").style.display = isAuthenticated ? "inline" : "none";
  document.getElementById("logout-link").style.display = isAuthenticated ? "inline" : "none";

  const welcome = document.getElementById("user-welcome-message");
  if (isAuthenticated) {
    document.getElementById("user-name").innerText = currentUser.name || "User";
    welcome.style.display = "inline";
  } else {
    welcome.style.display = "none";
  }
}

// Example usage on login form submission (add this in login.js after successful login)
document.getElementById("login-form").addEventListener("submit", function (e) {
  e.preventDefault();
  const email = this.querySelector('input[type="email"]').value;
  // You might fetch user name from backend; using dummy name here
  const dummyName = email.split('@')[0];
  login(dummyName); // Simulate login
});

