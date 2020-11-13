
function openLoginForm() {
    document.getElementById("login").style.display = "block";
}

function closeLoginForm() {
    document.getElementById("login").style.display = "none";
}

function toggleLoginRegisterOption() {
    var str = document.getElementById("login-register-toggle").innerHTML;
    if (!str.localeCompare("Registrace")) {
        // user wants to toggle to register
        document.getElementById("login-option").style.display = "none";
        document.getElementById("register-option").style.display = "block";
        document.getElementById("login-register-toggle").innerHTML = "Přihlášení";
    }
    else {
        //user wants to Login
        document.getElementById("register-option").style.display = "none";
        document.getElementById("login-option").style.display = "block";
        document.getElementById("login-register-toggle").innerHTML = "Registrace";
    }
}