function submitComment() {
    let authheader = Cookies.get('authheader');
    let comment = document.getElementById("commentInput").value;
    let postId = document.getElementsByClassName("post-container")[0].id;
    let body = {
        "comment": comment,
    }
    fetch("/posts/" + postId + "/comments/", {
        method: "post",
        headers: {
            "Content-Type": "application/json",
            'Authorization': `Basic ${authheader}`,

        },
        body: JSON.stringify(body)
    }).then((response) => {
        window.location = "/frontend/posts/" + postId
    });
}

function deletePost() {
    let authheader = Cookies.get('authheader');
    let postId = document.getElementsByClassName("post-container")[0].id;
    fetch("/posts/" + postId, {
        method: "delete",
        headers: {
            'Authorization': `Basic ${authheader}`,
        },
    }).then((response) => {
        window.location = "/frontend/posts/public/"
    });
}

function generateAuthorLinks() {
    let linkedElements = document.getElementsByClassName("author-link");
    for (let ele of linkedElements) {
        let eleParent = ele.parentNode;
        let anchor = document.createElement('a');

        user_id = ele.getAttribute("data-user");
        anchor.href = "/frontend/author/" + user_id + "/posts";
        anchor.className = "generated-author-link";
        // console.log(ele.href);

        eleParent.replaceChild(anchor, ele);
        anchor.appendChild(ele);
    }
}

function editPost() {
    if (!(document.getElementById("titleInput"))) {
        let titleInput = document.createElement("INPUT")
        titleInput.className = "addedInputs"
        titleInput.placeholder = "Enter a new title..."
        titleInput.id = "titleInput"

        let postInput = document.createElement("INPUT")
        postInput.className = "addedInputs"
        postInput.placeholder = "Enter a new post..."
        postInput.id = "postInput"

        let saveEditButton = document.createElement("BUTTON")
        saveEditButton.className = "btn btn-outline-primary"
        saveEditButton.innerText = "Save"
        saveEditButton.id = "saveButton"
        saveEditButton.onclick = saveEditPost;

        let cancelEditButton = document.createElement("BUTTON")
        cancelEditButton.className = "btn btn-outline-secondary"
        cancelEditButton.innerText = "Cancel"
        cancelEditButton.id = "cancelButton"
        cancelEditButton.onclick = cancelEditPost;

        document.getElementById("titleEditInput").appendChild(titleInput)
        document.getElementById("postEditInput").appendChild(postInput)
        document.getElementById("saveEditButton").appendChild(saveEditButton)
        document.getElementById("cancelEditButton").appendChild(cancelEditButton)
    }
}

function cancelEditPost() {
    document.getElementById("titleInput").remove()
    document.getElementById("postInput").remove()
    document.getElementById("saveButton").remove()
    document.getElementById("cancelButton").remove()
}

function saveEditPost() {
    // alert("save")
    let authheader = Cookies.get('authheader');
    let postId = document.getElementsByClassName("post-container")[0].id;
    console.log(postId)
    let editTitleText = document.getElementById("titleInput").value
    let editContentText = document.getElementById("postInput").value
    let body = {
        "title": editTitleText,
        "content": editContentText,
    };
    let edited = false;
    if (editTitleText !== '') {
        body.title = editTitleText;
        edited = true
    }
    if (editContentText !== '') {
        body.content = editContentText;
        edited = true
    }
    if (!(edited)) {
        return
    }

    fetch("/posts/" + postId, {
        method: "put",
        headers: {
            "Content-Type": "application/json",
            'Authorization': `Basic ${authheader}`,
        },
        body: JSON.stringify(body)
    }).then((response) => {
        window.location = "/frontend/posts/" + postId
    }, (err) => {
        console.log(err)
    })
}
