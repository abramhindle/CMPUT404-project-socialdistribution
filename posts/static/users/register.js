function registerUser() {
    let displayName = document.getElementById('displayName').value;
    let password1 = document.getElementById('password1').value;
    let password2 = document.getElementById('password2').value;
    let csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    if (validatePasswords(password1, password2)) {
        let body = {
            displayName: displayName,
            password1: password1,
            password2: password2,
            csrfmiddlewaretoken: csrf
        };
        console.log(body);
        fetch('/users/', {
            method: 'post',
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(body)
        }).then((response) => {
            return response.json()
        }).then((body) => {
            window.location = '/frontend/login'
        }, (error) => {
            // TODO Better error reporting
            for (let key in error) {
                console.log(error[key])
            }
        })
    } else {
        alert("Passwords do not match")
    }
}

function validatePasswords(password1, password2) {
    if (password1 !== password2) {
        return false
    } else if (password1 === '') {
        return false
    }
    return true
}