var encodedFile;
var getAuthorUrl;
var targetAuthor;

function getBase64(file, onLoadCallback) {
    return new Promise(function(resolve, reject) {
        var reader = new FileReader();
        reader.onload = function() { resolve(reader.result); };
        reader.onerror = reject;
        reader.readAsDataURL(file);
    });
}

function sendMessage(postUrl, postString = undefined, method = 'post'){
    return new Promise((resolve) => {
        fetch(postUrl,{
            method: method,
            headers: {
                'Content-Type' : 'application/json',
                'X-CSRFToken' : csrf_token
            },
            body: postString 

        })
        .then(function(response){
            //console.log(response);
            resolve(response.json());
        })
        .catch (function (error) {
            console.log('Request failed', error);
        });
    }) 
}

function buildAuthor(){
    var displayName = document.getElementById("displayName").value;
    var github = document.getElementById("github").value;
    var isApproved = document.getElementById("isApproved").checked;
    
    targetAuthor.displayName = displayName;
    targetAuthor.github = github;
    targetAuthor.profileImage = encodedFile;
    targetAuthor.isApproved = isApproved;
}

function refresh(author){
    targetAuthor = author;
    encodedFile = targetAuthor.profileImage;
    document.getElementById("displayName").value = targetAuthor.displayName;
    document.getElementById("github").value = targetAuthor.github;
    document.getElementById("profileImage").src = encodedFile;
    document.getElementById("isApproved").checked = targetAuthor.isAdmin || targetAuthor.isApproved

    document.getElementById("displayNameP").innerText = targetAuthor.displayName;
    document.getElementById("githubP").innerText = targetAuthor.github;
    document.getElementById("host").innerText = targetAuthor.host;
    document.getElementById("isAdmin").innerText = targetAuthor.isAdmin ? "True" : "False";
    if (author_id != target_author_id){
        document.getElementById("followbutton").innerText = is_following ? "Unfollow" : "Follow"
    }
    if (targetAuthor.isAdmin){
        document.getElementById("isApprovedSection").className = "hidden"
    }
}

function toggleEditting(editing){
    var displayClass = "displaying"
    var editClass = "editing"
    var isApprovedEl = document.getElementById("isApproved")
    if (editing) {
        displayClass += " hidden"
        isApprovedEl.disabled = false;
    }
    else{
        editClass += " hidden"
        isApprovedEl.disabled = true;
    }

    var displayElements = document.getElementsByClassName('displaying');
    for (var i in displayElements){
        if (displayElements.hasOwnProperty(i)) {
            displayElements[i].className = displayClass;
        }
    }

    var editElements = document.getElementsByClassName('editing');
    for (var i in editElements){
        if (editElements.hasOwnProperty(i)) {
            editElements[i].className = editClass;
        }
    }
}

$(document).ready(function() {
    targetAuthorUrl = host+'/author/'+target_author_id;
    sendMessage(targetAuthorUrl, undefined, "get").then(function(response){
        if (response){
            refresh(response);
        }
    });

    document.getElementById("profileImageFile").onchange = function() {
        var file = document.getElementById("profileImageFile").files[0];
        getBase64(file).then(function(result) {
            if (result){
                encodedFile=result;
                img = document.getElementById("profileImage")
                img.src = encodedFile;
            }
        });
    };
    
    document.getElementById("submitbutton").onclick = function(){
        buildAuthor();
        var postString = JSON.stringify(targetAuthor);
        sendMessage(targetAuthorUrl, postString).then(function(response){
            if (response){
                refresh(response);
            }
        });
        toggleEditting(false);
    };
    
    document.getElementById("editbutton").onclick = function(){
        toggleEditting(true);
    };

    if (author_id != target_author_id){
        followUrl = host+'/author/'+target_author_id+"/followers/"+author_id;
        document.getElementById("followbutton").onclick = function(){
            if (is_following){
                sendMessage(followUrl, undefined, "delete");
            }
            else{
                sendMessage(followUrl, undefined, "put");
            }
            
            is_following = is_following ? false : true
            document.getElementById("followbutton").innerText = is_following ? "Unfollow" : "Follow"
        };
    }

    document.getElementById("isApproved").onchange = function() {
        var checked = document.getElementById("isApproved").checked;
        getBase64(file).then(function(result) {
            if (result){
                encodedFile=result;
                img = document.getElementById("profileImage")
                img.src = encodedFile;
            }
        });
    };
});
