
function openLoginForm() {
    document.getElementById("login-window").style.display = "block";
    document.getElementById("blur").style.filter = "blur(10px)";
}

function closeLoginForm() {
    document.getElementById("login-window").style.display = "none";
    document.getElementById("blur").style.filter = "blur(0px)";
}

function toggleLoginRegisterOption() {
    var str = document.getElementById("login-register-toggle").innerHTML;
    if (!str.localeCompare("Registrace")) {
        // user wants to toggle to login
        console.log("going to login")  ;
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

function userCreateController() {
    var obj = document.getElementById("dash_user_employee_check");

    if (obj.checked == false){
        for(let i = 0; i < 4; i++) {
            obj = obj.nextElementSibling;
            obj.disabled = true;
        }
    }
    else {
        for(let i = 0; i < 4; i++) {
            obj = obj.nextElementSibling;
            obj.disabled = false;
        }
    }
}

function updatePrice(object_, price) {
    var date_from = new Date(document.getElementById("date_from").value);
    var date_to = new Date(document.getElementById("date_to").value);
    var rooms = document.getElementById("one_rooms").value;

    today = new Date();
    today.setHours(0,0,0,0);

    if (date_from && date_to && date_from >= today && date_to >= today && date_to > date_from) {
        var diff = ((((date_to - date_from) / 1000) / 60) / 60) / 24
        object_.innerHTML = (diff * price * rooms)
    }
}