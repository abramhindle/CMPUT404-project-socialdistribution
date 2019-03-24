function addPrivate() {
    // structure reference for each input box
    // div
    //     privateDiv
    //         removeButtonDiv
    //             removeButton
    //         option
    
    let div = document.getElementById("append");
    let privateDiv = document.createElement('div');
    let removeButtonDiv = document.createElement("div");
    let removeButton = document.createElement("button");
    let option = document.createElement("input");
    option.classList.add('form-control');
    option.name = "visibleTo[]";
    option.value = "";

    removeButtonDiv.className = "input-group-append";
    removeButton.className = "btn btn-danger";
    removeButton.onclick = deleteParent;
    removeButtonDiv.appendChild(removeButton);

    privateDiv.className = "input-group";
    privateDiv.appendChild(option);
    privateDiv.appendChild(removeButtonDiv);

    div.appendChild(privateDiv);
}

function deleteParent() {
    this.parentNode.parentNode.remove()
}

// not working, cant handle redirects
function submitForm() {
    let files = document.getElementById('files')
    if (files.files.length > 0) {
        let fileList = [...files.files];
        let filePromises = getFiles(fileList);
        let postPromises = filePromises.then((files) => {
            return Promise.all(files.map(file => postImage(file)));
        });
        postPromises.then((json) => {
            let imageIDs = json.map(post => {
                return post.id;
            });
            makePost(imageIDs)
        })
    } else {
        makePost();
    }
}

function makePost(imageIDs = undefined) {
    let content;
    let title = document.getElementById('title').value;
    let description = document.getElementById('description').value;
    let contentType = document.getElementById('contentType').value;
    let visibility = document.getElementById('visibility').value;
    let unlisted = document.getElementById('unlisted').checked;
    let csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    let visibleToArray = [];

    if (visibility === "PRIVATE") {
        visibleTo = document.getElementsByName('visibleTo[]');
        for (let element of visibleTo) {
            visibleToArray.push(element.value);
        }
    } else {
    }
    if (imageIDs !== undefined) {
        imageIDs = imageIDs.map((id) => {
            return window.location.origin + '/posts/' + id + '\n';
        });
        content = imageIDs.join(' ') + '\n' + document.getElementById('content').value;

    } else {
        content = document.getElementById('content').value;
    }
    let body = {
        title: title,
        description: description,
        content: content,
        contentType: contentType,
        unlisted: unlisted,
        visibility: visibility,
        visibleTo: visibleToArray,
        csrfmiddlewaretoken: csrf,
    };
    fetch('/posts/', {
        method: 'post',
        headers: {
            "X-CSRFToken": csrf,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(body)
    }).then((res) => {
        return res.json()
    }).then((json) => {
        console.log(json);
        window.location.href = '/frontend/posts/' + json.id
    }, (err) => {
        console.log(err)
    })
}

function postImage(fileContent) {
    return new Promise((resolve, reject) => {

        let fileType = fileContent.split(':')[1].split(';')[0];
        fileType += ';base64';
        let formData = new FormData();
        let visbility = document.getElementById('visibility').value;
        let csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value;
        formData.append('title', 'Image"');
        formData.append('content', fileContent);
        formData.append('description', 'Image');
        formData.append('unlisted', 'true');
        formData.append('contentType', fileType);
        formData.append('visbility', visbility);
        formData.append('csrfmiddlewaretoken', csrf);
        fetch('/posts/', {
            method: 'post',
            body: formData,
            headers: {
                "X-CSRFToken": csrf
            }
        }).then((response) => {
                resolve(response.json())
            }, (error) => {
                console.log(error)
            }
        )
    })

}

// https://stackoverflow.com/users/1894471/dmitri-pavlutin
// https://stackoverflow.com/questions/36280818/how-to-convert-file-to-base64-in-javascript
function getBase64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => resolve(reader.result);
        reader.onerror = error => reject(error);
    });
}

function getFiles(files) {
    return Promise.all(files.map(file => getBase64(file)));
}

function checkPrivate() {
    if (document.getElementById('visibility').value === 'PRIVATE') {
        document.getElementById('private-urls').style.display = 'block';
    } else {
        document.getElementById('private-urls').style.display = 'none';
    }
}
