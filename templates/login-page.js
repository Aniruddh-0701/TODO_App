const loginForm = document.getElementById("login-form");
const loginButton = document.getElementById("submit-form");
const loginErrorMsg = document.getElementById("error-display");

loginButton.addEventListener("click", (e) => {
    e.preventDefault();
    const username = loginForm.username.value;
    const password = loginForm.password.value;

    if (isLowerCase(username)) {
        alert("You have successfully logged in.");
        location.reload();
    } else {
        loginErrorMsg.style.opacity = 1;
    }
})