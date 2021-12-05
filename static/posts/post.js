$(document).ready(function() {
    posts = document.querySelectorAll('div.post')

    posts.forEach((post) => {
        let postId = post.getAttribute("post-id");
        let authorOfPostId = post.getAttribute("author-id");
        let userAuthorId = user_author;

        // Add like button functionality
        let likeButton = document.getElementById(postId + '-like-button');
        likeButton.onclick = async function() {
            if (user_authenticated == "True") {                
                await likePost(postId, authorOfPostId, userAuthorId);

                // update with actual user
                await updateLikedPost(postId, authorOfPostId, userAuthorId);

            } else {
                alert("You need to Log In");
            }   
        };

        // Set like to liked class if already liked
        if (user_authenticated == "True") {
            checkLikedClassPost(postId, host + '/author/' + userAuthorId);
        }

        // Add comment button functionality
        let addCommentButton = document.getElementById('addcomment-' + postId);
        addCommentButton.onclick = async function() {
            if (user_authenticated == "True") {      
                let commentText = prompt("Add comment here"); 
                if (commentText != null) {
                    await commentPost(commentText, postId, authorOfPostId, userAuthorId);
                    await updateComments(commentText, postId, userAuthorId);
                }
            } else {
                alert("You need to Log In");
            }
        };
    });
});

async function likePost(postId, authorOfPostId, userAuthorId) {
    let like = new Object();
    
    // Get author of the user requesting the like
    let getAuthorUrl = host + '/author/' + userAuthorId;
    await fetch(getAuthorUrl, {
        method: 'get',
        headers: {
            'Content-Type' : 'application/json',
            'X-CSRFToken' : csrf_token
        }
    })
    .then(function(authorResponse) {
        return authorResponse.json();
    })
    .then(async function(authorLikingPost) {

        // Get post being liked
        let getPostUrl = host + '/author/' + authorOfPostId + '/posts/' + postId + '/';
        return await fetch(getPostUrl, {
            method: 'get',
            headers: {
                'Content-Type' : 'application/json',
                'X-CSRFToken' : csrf_token
            }
        })
        .then(postResponse => {
            return postResponse.json();
        })
        .then(async function(postData) {
            let post = postData.data;
            like.author = authorLikingPost;
            // this id contains proper link to obj
            like.object = post.id;
            likeStr = JSON.stringify(like);
    
            // Post like to the inbox of its author
            let postLikeUrl = post.author.url + '/inbox/';
            return await fetch(postLikeUrl, {
                method: 'POST',
                headers: {
                    'Content-Type' : 'application/json',
                    'X-CSRFToken' : csrf_token
                },
                body: likeStr
            });
        });
    });
}

async function commentPost(commentText, postId, authorOfPostId, userAuthorId) {
    if (commentText != null) {
        let comment = new Object();
        comment.comment = commentText;
        comment.type = "comment";
        comment.contentType = "text/plain";
        
        // Get author of the user requesting the comment
        let url = host + '/author/' + userAuthorId;
        fetch(url, {
            method: 'get',
            headers: {
                'Content-Type' : 'application/json',
                'X-CSRFToken' : csrf_token
            }
        })
        .then(function(authorResponse) {
            return authorResponse.json();
        })
        .then(function(authorData) {
            comment.author = authorData;
            commentStr = JSON.stringify(comment);

            // Post comment
            url = host + '/author/' + authorOfPostId + '/posts/' + postId + '/comments/';
            return fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type' : 'application/json',
                    'X-CSRFToken' : csrf_token
                },
                body: commentStr
            })
        })
        .then(function(){
            alert("Comment posted!");
        })
        .catch(function(e){
            console.log("Error", e);
        });
    };
}

async function updateLikedPost(postId, authorOfPostId, userAuthorId) {
    let userAuthorUrl = host + '/author/' + userAuthorId;
    let authorOfPostUrl = host + '/author/' + authorOfPostId;
    await checkLikedClassPost(postId, userAuthorUrl);
    await checkLikeCountPost(postId, authorOfPostUrl);
}

async function updateComments(commentText, postId, userAuthorId) {
    await checkCommentsSection(commentText, postId, userAuthorId);
}

async function checkCommentsSection(commentText, postId, userAuthorId) {
    // Get author of user to extract name
    let url = host + '/author/' + userAuthorId;
    author = await fetch(url, {
        method: 'get',
        headers: {
            'Content-Type' : 'application/json',
            'X-CSRFToken' : csrf_token
        }
    })  
    .then(function(authorResponse) {
        return authorResponse.json();
    });

    // build div with class "comment" and Author name as link and comment inside
    let commentsDiv = document.getElementById("comments-of-" + postId);
    var commentDiv = document.createElement('div');
    var commentP = document.createElement('p');
    
    posteeLink = host + '/site/authors/' + userAuthorId;
    posteeLinkTag = "<a class=\"author-link\" href=\"" + posteeLink + "\">" + author.displayName + "</a>";
    commentP.innerHTML = posteeLinkTag + ": " + commentText; 
    
    commentDiv.appendChild(commentP);
    commentDiv.classList.add('comment');
    
    commentsDiv.insertChildAtIndex(commentDiv, 0);
    
    // Remove latest comment if oversize
    if (commentsDiv.childElementCount > commentsSectionSize) {
        commentsDiv.removeChild(commentsDiv.lastElementChild);
    }
}

async function checkLikedClassPost(postId, userAuthorUrl) {
    let likeButton = document.getElementById(postId + '-like-button');
    let ifLikesPost = await userLikesPost(postId, userAuthorUrl)
    if (ifLikesPost) {
        likeButton.classList.remove("liked");
        likeButton.classList.add("liked");
    }
}

async function checkLikeCountPost(postId, authorOfPostUrl) {
    let likeCountSpan = document.getElementById("like-count-" + postId);
    let likes = await getLikesPost(postId, authorOfPostUrl);

    likeCountSpan.innerHTML = likes.length;   
}

async function userLikesPost(postId, authorUrl) {
    let url = authorUrl + '/liked';
    let likedB = false;
    await fetch(url, {
        method: 'get',
        headers: {
            'Content-Type' : 'application/json',
            'X-CSRFToken' : csrf_token
        }
    })
    .then(likedResponse => {
        return likedResponse.json();
    })
    .then(function(likedData) {
        let liked = likedData.data;
        
        liked.forEach(likedEntity => {
            let likedEntityUrl = likedEntity.object;
            const postIdRegex = /post(s)?\/(?<id>.[^\/]*)(\/)?$/g;
            let res = postIdRegex.exec(likedEntityUrl);

            // Match regexed id of a liked entity to given post id
            if (res && res.groups && res.groups.id) {
                if (postId == res.groups.id) {
                    likedB = true;
                }
            }
        });
    })

    return likedB;
}

async function getLikesPost(postId, authorUrl) {
    let url = authorUrl + "/post/" + postId + '/likes';
    let likes = [];

    await fetch(url, {
        method: 'get',
        headers: {
            'Content-Type' : 'application/json',
            'X-CSRFToken' : csrf_token
        }
    })
    .then(likesResponse => {
        return likesResponse.json();
    })
    .then(function(likesData) {
        likes = likesData.data;
    })

    return likes;
}

// Insert child in a specific index
// https://stackoverflow.com/questions/5882768/how-to-append-a-childnode-to-a-specific-position
Element.prototype.insertChildAtIndex = function(child, index) {
    if (!index) index = 0
    if (index >= this.children.length) {
      this.appendChild(child)
    } else {
      this.insertBefore(child, this.children[index])
    }
}