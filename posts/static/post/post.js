function submitComment() {
    let comment = document.getElementById("commentInput").value;
    let postId = document.getElementsByClassName("post-container")[0].id;
    let csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value;    
    let body = {
        "comment": comment,
        "csrfmiddlewaretoken": csrf,
    }
    fetch("/posts/" + postId + "/comments/", {
        method: "post",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken" : csrf,

        },
        body: JSON.stringify(body)
    }).then((response) => {
        window.location = "/frontend/posts/" + postId
    });
}
