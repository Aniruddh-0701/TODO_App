function ValidateLogin() {
    const username = document.getElementById("uid").value;
    const password = document.getElementById("pwd").value;
    if (username != "" && password != ""){
        if (username != username.toUpperCase()) {
            return true;
        } else {
            alert("Invalid Username format");
            return false;
        }
    }else{
        alert("Please enter a UID and Password");
        return false;
    }
}

function ValidateName(name){
    var regex = /^[A-Za-z\t]+$/;
 
        //Validate TextBox value against the Regex.
        var isValid = regex.test(document.getElementById(name).value);
        if (!isValid) {
            alert("Only Alphabets allowed.");
        }
 
        return isValid;
}

function ValidateUID(){
    var regex = /^[a-z0-9_@$-]+$/;
 
        //Validate TextBox value against the Regex.
        var isValid = regex.test(document.getElementById("uid").value);
        if (!isValid) {
            const str = 'The ID should consist of \n'+
                'One Lowercase Alphabet a-z\n'+
                'One digit 0-9\n'+
                '(Optional) One Special Character @, _, $';
            alert(str);
        }
 
        return isValid;
}

function ValidatePwd(){
    var regex = /^[A-Za-z0-9@_]+$/;
 
        //Validate TextBox value against the Regex.
        var pwd = document.getElementById("pwd").value;
        var isValid = regex.test(pwd);
        if (!isValid) {
            const str = 'The Password should consist of \n'+
                'One Lowercase Alphabet a-z\n'+
                'One Uppercase Alphabet A-Z\n'+
                'One digit 0-9\n'+
                'One Special Character @, _';
            alert(str);
        }
 
        return isValid;
}

function ValidPwd(){
    var pwd = document.getElementById("pwd").value;
    if(pwd.length < 8 || pwd.length > 16){
        alert("The Password should contain 8 - 16 characters only");
    }
}

function showPwd() {
    var x = document.getElementById("pwd");
    if (x.type === "password") {
      x.type = "text";
    } else {
      x.type = "password";
    }
  }
  
