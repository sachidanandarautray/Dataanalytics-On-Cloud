function togglePasswordVisibility(inputId) {
  const input = document.getElementById(inputId);
  if (input.type === "password") {
    input.type = "text";
  } else {
    input.type = "password";
  }
}

function checkPasswordMatch() {
  const password = document.getElementById("password").value;
  const confirmPassword = document.getElementById("confirmPassword").value;
  const passwordError = document.getElementById("passwordError");
  const submitButton = document.getElementById("submitButton"); // Get the submit button element

  if (password !== confirmPassword) {
    passwordError.textContent = "Passwords do not match.";
    submitButton.disabled = true; // Disable the submit button
  } else {
    passwordError.textContent = "";
    submitButton.disabled = false; // Enable the submit button
  }
}
