function follow_user(other, user) {
    let csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    let body = {
        author: user,
        friend: other,
        csrfmiddlewaretoken: csrf
    };
    fetch('/friendrequest/', {
        method: 'post',
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrf,
        },
        body: JSON.stringify(body)
    }).then((res) => {
        window.location.reload(true)
    });
}

function unfollow_user(id) {
    let csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    let body = {
        csrfmiddlewaretoken: csrf
    };
    fetch(`/follow/${id}/`, {
        method: 'delete',
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrf,
        },
        body: JSON.stringify(body)
    }).then((res) => {
        window.location.reload(true)
    });
}
