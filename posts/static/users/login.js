function loginUser() {
    let displayName = document.getElementById('displayName').value;
    let password = document.getElementById('password').value;
    let csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value;
        let body = {
            username: displayName,
            password: password,
            csrfmiddlewaretoken: csrf,
            submit: "Log in"
        }
        fetch('/api-auth/login/', {
            method: 'post',
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken" : csrf,
            },
            body: JSON.stringify(body)
        }).then((response) => {
            console.log(response);
        }).then((body) => {
            //window.location = '/posts'
        }, (error) => {
            // TODO Better error reporting
            for (let key in error) {
                console.log(error[key])
            }
        })
}

