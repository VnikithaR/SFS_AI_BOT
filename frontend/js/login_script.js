// Validation functions
function validateEmail(email) {
  const regex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
  return regex.test(email);
}

function validatePassword(password) {
  // Password should be at least 8 characters, contain at least one number, one uppercase letter, and one special character
  const regex = /^(?=.*[A-Z])(?=.*[0-9])(?=.*[\W_]).{8,}$/;
  return regex.test(password);
}

function validateForm(formName) {
  const email = document.querySelector(`${formName} input[type="text"]`).value;
  const password = document.querySelector(`${formName} input[type="password"]:first-of-type`).value;
  let confirmPassword = '';
  if (formName === '.signup') {
      confirmPassword = document.querySelector(`${formName} input[type="password"]:last-of-type`).value;
  }
  
  // Check if required fields are filled
  if (!email || !password || (formName === '.signup' && !confirmPassword)) {
      displayMessage(formName, 'All fields are required', 'error');
      return false;
  }

  // Validate email
  if (!validateEmail(email)) {
      displayMessage(formName, 'Invalid email format', 'error');
      return false;
  }

  // Validate password
  if (!validatePassword(password)) {
      displayMessage(formName, 'Password must contain at least 8 characters, 1 uppercase, 1 number, and 1 special character', 'error');
      return false;
  }

  // Confirm password check for signup
  if (formName === '.signup' && password !== confirmPassword) {
      displayMessage(formName, 'Passwords do not match', 'error');
      return false;
  }

  return true;
}

// Display message
function displayMessage(formName, message, type) {
  const messageElement = document.createElement('div');
  messageElement.classList.add(type);
  messageElement.textContent = message;
  const form = document.querySelector(formName);
  const existingMessage = form.querySelector('.message');
  if (existingMessage) {
      existingMessage.remove();
  }
  form.insertBefore(messageElement, form.firstChild);
  setTimeout(() => {
      messageElement.remove();
  }, 5000);
}

// Clear form fields
function clearForm(formName) {
  const form = document.querySelector(formName);
  form.reset();
}

// Handle form submissions
function handleLoginSubmit(event) {
  event.preventDefault();
  
  if (validateForm('.login')) {
      // Simulate success response (e.g., make an API call to backend here)
      displayMessage('.login', 'Login successful!', 'success');
      clearForm('.login');
  }
}

function handleSignupSubmit(event) {
  event.preventDefault();
  
  if (validateForm('.signup')) {
      // Simulate success response (e.g., make an API call to backend here)
      displayMessage('.signup', 'Signup successful!', 'success');
      clearForm('.signup');
  }
}

// Switch between login and signup forms
document.getElementById('login').addEventListener('change', function () {
  document.querySelector('.login').style.display = 'block';
  document.querySelector('.signup').style.display = 'none';
});
document.getElementById('signup').addEventListener('change', function () {
  document.querySelector('.signup').style.display = 'block';
  document.querySelector('.login').style.display = 'none';
});

// Attach event listeners to forms
document.querySelector('.login form').addEventListener('submit', handleLoginSubmit);
document.querySelector('.signup form').addEventListener('submit', handleSignupSubmit);
