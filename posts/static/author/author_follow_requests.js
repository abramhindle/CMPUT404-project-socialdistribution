function delete_follow_request(target_user) {
    let csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    let body = {
        csrfmiddlewaretoken: csrf
    };
    fetch(`/frontend/friendrequest/${target_user}/`, {
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