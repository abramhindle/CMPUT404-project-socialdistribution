function loginUser() {
    let displayName = document.getElementById('displayName').value;
    let password = document.getElementById('password').value;
    let body = {
        username: displayName,
        password: password,
    }
    fetch('/frontend/login/', {
        method: 'post',
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(body)
    }).then((response) => {
        let base64 = btoa(`${displayName}:${password}`);
        Cookies.set('authheader', base64);
        window.location = '/frontend/posts/public/';
    }).then((body) => {
        return body;
    }, (error) => {
        // TODO Better error reporting
        for (let key in error) {
            console.log(error[key])
        }
    })
}

