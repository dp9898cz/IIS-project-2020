
function openLoginForm() {
    document.getElementById("login-window").style.display = "block";
}

function closeLoginForm() {
    document.getElementById("login-window").style.display = "none";
}

function fixMultiFormsIDs() {
    try {
        var str = document.getElementById("login-register-toggle").innerHTML;
        if (str.localeCompare("Registrace")) {
            // user wants to register
            document.querySelector("#login-option > form > input[type=hidden]:nth-child(1)").setAttribute("id", "#csrf_token_2");
            document.querySelector("#login-option > form > input[name=submit]").setAttribute("id", "#submit_2");
            document.querySelector("#register-option > form > input[type=hidden]:nth-child(1)").setAttribute("id", "#csrf_token");
            document.querySelector("#register-option > form > input[name=submit]").setAttribute("id", "#submit");
        }
        else {
            // user wants to login
            document.querySelector("#login-option > form > input[type=hidden]:nth-child(1)").setAttribute("id", "#csrf_token");
            document.querySelector("#login-option > form > input[name=submit]").setAttribute("id", "#submit");
            document.querySelector("#register-option > form > input[type=hidden]:nth-child(1)").setAttribute("id", "#csrf_token_2");
            document.querySelector("#register-option > form > input[name=submit]").setAttribute("id", "#submit_2");
        }
    }
    catch {
        console.log("ERROR: form not defined")
    }
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
    fixMultiFormsIDs();
}