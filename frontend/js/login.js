document.addEventListener('DOMContentLoaded', function () {
    // Elements
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
    const passwordSignup = signupForm.querySelector('input[type="password"]');
    const confirmPasswordSignup = signupForm.querySelectorAll('input[type="password"]')[1];

    // Simulate user database using localStorage
    let users = JSON.parse(localStorage.getItem("users")) || [];

// Show Login Modal
loginBtn.addEventListener("click", function (e) {
    e.preventDefault();

    // Only show login if we're not already showing forgot password
    if (!document.body.classList.contains("forgot-password-active")) {
        document.body.classList.add("login-active");
        overlay.style.display = "block";
        loginWrapper.style.display = "block";
        toggleAuthTabs(); // This ensures the correct tab is shown
    }
});

    // Toggle Login/Signup Tabs
    loginTab.addEventListener("change", toggleAuthTabs);
    signupTab.addEventListener("change", toggleAuthTabs);

    function toggleAuthTabs() {
        if (loginTab.checked) {
            loginForm.style.display = "block";
            signupForm.style.display = "none";
        } else {
            loginForm.style.display = "none";
            signupForm.style.display = "block";
        }
    }

    // Close modals
    overlay.addEventListener("click", closeModal);
    closeModalBtn.addEventListener("click", closeModal);

    function closeModal() {
        document.body.classList.remove("login-active", "forgot-password-active");
        overlay.style.display = "none";
        loginWrapper.style.display = "none";
        forgotPasswordModal.style.display = "none";
    }

    // Show Forgot Password Modal
    forgotPasswordLink.addEventListener("click", function (e) {
        e.preventDefault();
        document.body.classList.add("forgot-password-active");
        forgotPasswordModal.style.display = "block";
        overlay.style.display = "block";
    });

    // Toggle Login/Signup via inline text links
    const loginLink = document.querySelector(".login-link");
    const signUpLink = document.querySelector(".sign-up-link");

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

    // Password Visibility Toggles
    if (passwordToggleLogin) {
        passwordToggleLogin.addEventListener("click", function () {
            const type = passwordLogin.type === "password" ? "text" : "password";
            passwordLogin.type = type;
            this.classList.toggle("show-password");
        });
    }

    if (passwordToggleSignup) {
        passwordToggleSignup.addEventListener("click", function () {
            const type = passwordSignup.type === "password" ? "text" : "password";
            const confirmType = confirmPasswordSignup.type === "password" ? "text" : "password";
            passwordSignup.type = type;
            confirmPasswordSignup.type = confirmType;
            this.classList.toggle("show-password");
        });
    }

    // Handle Login Submit
    loginForm.addEventListener("submit", function (e) {
        e.preventDefault();
        const email = this.querySelector('input[type="email"]').value.trim();
        const password = this.querySelector('input[type="password"]').value.trim();

        if (!validateEmail(email)) {
            alert("Please enter a valid email.");
            return;
        }

        const user = users.find(u => u.email === email && u.password === password);
        if (user) {
            alert("Login successful!");
            closeModal();
        } else {
            alert("Invalid email or password.");
        }
    });

    // Handle Signup Submit
    signupForm.addEventListener("submit", function (e) {
        e.preventDefault();
        const fullName = this.querySelector('input[placeholder="Full Name"]').value.trim();
        const email = this.querySelectorAll('input[type="email"]')[1].value.trim();
        const password = this.querySelectorAll('input[type="password"]')[0].value.trim();
        const confirmPassword = this.querySelectorAll('input[type="password"]')[1].value.trim();

        if (fullName === "" || email === "" || password === "" || confirmPassword === "") {
            alert("Please fill out all fields.");
            return;
        }

        if (password !== confirmPassword) {
            alert("Passwords do not match.");
            return;
        }

        if (users.find(u => u.email === email)) {
            alert("Email already exists.");
            return;
        }

        const newUser = { fullName, email, password };
        users.push(newUser);
        localStorage.setItem("users", JSON.stringify(users));
        alert("Signup successful!");
        loginTab.checked = true;
        toggleAuthTabs();
    });

    // Handle Reset Password
    resetPasswordForm.addEventListener("submit", function (e) {
        e.preventDefault();
        const email = this.querySelector('input[type="email"]').value.trim();

        if (!validateEmail(email)) {
            alert("Please enter a valid email.");
            return;
        }

        const userIndex = users.findIndex(user => user.email === email);
        if (userIndex === -1) {
            alert("Email not found.");
            return;
        }

        const newPassword = prompt("Enter new password:");
        if (newPassword) {
            users[userIndex].password = newPassword;
            localStorage.setItem("users", JSON.stringify(users));
            alert("Password reset successful.");
            closeModal();
        }
    });

    function validateEmail(email) {
        const emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
        return emailPattern.test(email);
    }

    // Initialize tab visibility on load
    toggleAuthTabs();
});
