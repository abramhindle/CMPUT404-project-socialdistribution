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
                    commentResp = await commentPost(commentText, postId, authorOfPostId, userAuthorId);
                    
                    let commentId = getCommentId(commentResp.data.id);
                    await updateComments(commentText, commentId, postId, userAuthorId);
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
        let getPostUrl = postId;
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
            let post = postData.data.length && postData.data.length > 0 ? postData.data[0] : postData.data;
            like.author = authorLikingPost;
            // this id contains proper link to obj
            like.object = post.id;
            like.type = "like"
            likeStr = JSON.stringify(like);
    
            // Post like to the inbox of its author
            let postLikeUrl =  host + '/author/' + post.author.url + '/inbox';
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
        let commentResp = null;
        comment.comment = commentText;
        comment.type = "comment";
        comment.contentType = "text/plain";
        
        // Get author of the user requesting the comment
        let url = host + '/author/' + userAuthorId;
        await fetch(url, {
            method: 'get',
            headers: {
                'Content-Type' : 'application/json',
                'X-CSRFToken' : csrf_token
            }
        })
        .then(function(authorResponse) {
            return authorResponse.json();
        })
        .then(async function(authorData) {
            comment.author = authorData;
            comment.type = "comment"
            comment.id = postId + '/comment/';
            commentStr = JSON.stringify(comment);

            // Post comment
            url = host + '/author/' + authorOfPostId + '/inbox';
            commentResp = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type' : 'application/json',
                    'X-CSRFToken' : csrf_token
                },
                body: commentStr
            })
            .then(function(postResponse) {
                return postResponse.json();
            })

            return commentResp;
        })
        .then(function(){
            alert("Comment posted!");
        })
        .catch(function(e){
            console.log("Error", e);
        });

        return commentResp;
    };
}

async function updateLikedPost(postId, authorOfPostId, userAuthorId) {
    let userAuthorUrl = host + '/author/' + userAuthorId;
    let authorOfPostUrl = host + '/author/' + authorOfPostId;
    await checkLikedClassPost(postId, userAuthorUrl);
    await checkLikeCountPost(postId, authorOfPostUrl);
}

async function updateComments(commentText, commentId, postId, userAuthorId) {
    await buildCommentsSection(commentText, commentId, postId, userAuthorId);
}

async function buildCommentsSection(commentText, commentId, postId, userAuthorId) {
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

    var likeCountSpan = document.createElement('span');
    likeCountSpan.innerHTML = "0";
    likeCountSpan.setAttribute('id', 'like-count-comment-' + commentId);
    
    var likeButton = document.createElement('button');
    likeButton.innerHTML = " | Like";
    likeButton.prepend(likeCountSpan);
    likeButton.classList.add('btn');
    likeButton.setAttribute('id', commentId + '-comment-like-button');
    likeButton.setAttribute('type', 'submit');
    likeButton.setAttribute('name', 'comment_id');
    likeButton.setAttribute('value', commentId);
    
    commentDiv.appendChild(likeButton);
    commentDiv.appendChild(commentP);
    commentDiv.classList.add('comment');
    commentDiv.setAttribute('author-comment-id', userAuthorId);
    commentDiv.setAttribute('comment-id', commentId);
    
    commentsDiv.insertChildAtIndex(commentDiv, 0);
    
    // Remove latest comment if oversize
    if (commentsDiv.childElementCount > commentsSectionSize) {
        commentsDiv.removeChild(commentsDiv.lastElementChild);
    }

    setupCommentsLikes()
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

    likeCountSpan.innerHTML = likes ? likes.length : 0;   
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
            if (postId == getPostId(likedEntityUrl)) {
                likedB = true;
            }
        });
    })

    return likedB;
}

function getPostId(postId) {
    const postIdRegex = /post(?:s)?\/([^\/]*)(?:\/)?(?:.*)$/g;
    let res = postIdRegex.exec(postId);

    // Match regexed id of a liked entity to given post id
    if (res && res.groups && res.groups.id) {
        return res.groups.id
    }

    return null;
}

function getCommentId(commentId) {
    const commentIdRegex = /comment(?:s)?\/([^\/]*)(?:\/)?(?:.*)$/g;
    let res = commentIdRegex.exec(commentId);

    // Match regexed id of a liked entity to given post id
    if (res && res.groups && res.groups.id) {
        return res.groups.id
    }

    return null;
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

// Likes related to comments below

$(document).ready(function() {
    setupCommentsLikes()
});

async function setupCommentsLikes() {
    commentSections = document.querySelectorAll('div.comments')

    let userAuthorId = user_author;
    commentSections.forEach((commentSection) => {
        let postId = commentSection.getAttribute("post-id");
        let authorOfPostId = commentSection.getAttribute("author-post-id");
        
        let comments = [...commentSection.children];
        comments.forEach(function(comment) {
            let commentId = comment.getAttribute("comment-id");
            let authorOfCommentId = comment.getAttribute("author-comment-id");
            
            // Add like button functionality
            let likeButton = document.getElementById(commentId + "-comment-like-button");
            likeButton.onclick = async function() {
                if (user_authenticated == "True") {  
                    // Like the thing              
                    await likeComment(postId, commentId, authorOfPostId, userAuthorId);

                    // update class and count
                    await updateLikedComment(postId, commentId, authorOfPostId, userAuthorId);

                } else {
                    alert("You need to Log In");
                }   
            };

            // Set like to liked class if already liked
            if (user_authenticated == "True") {
                checkLikedClassComment(commentId, host + '/author/' + userAuthorId);
            }
        
        });
    });
}

async function updateLikedComment(postId, commentId, authorOfPostId, userAuthorId) {
    let userAuthorUrl = host + '/author/' + userAuthorId;
    let authorOfPostUrl = host + '/author/' + authorOfPostId;
    await checkLikedClassComment(commentId, userAuthorUrl);
    await checkLikeCountComment(postId, commentId, authorOfPostUrl);
}

async function checkLikeCountComment(postId, commentId, authorOfPostUrl) {
    let likeCountSpan = document.getElementById("like-count-comment-" + commentId);
    let likes = await getLikesComment(postId, commentId, authorOfPostUrl);
    
    likeCountSpan.innerHTML = likes ? likes.length : 0;   
}

async function checkLikedClassComment(commentId, userAuthorUrl) {
    let likeButton = document.getElementById(commentId + '-comment-like-button');
    let ifLikesComment = await userLikesComment(commentId, userAuthorUrl)
    if (ifLikesComment) {
        likeButton.classList.remove("liked");
        likeButton.classList.add("liked");
    }
}

async function likeComment(postId, commentId, authorOfPostId, userAuthorId) {
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

        // Get post above comment being liked
        let getPostUrl = postId;
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
            like.type = "like";
            like.author = authorLikingPost;
            // this id contains proper link to the parent post
            like.object = post.id + "/comments/" + commentId;
            likeStr = JSON.stringify(like);
    
            // Post like to the inbox of its author
            let postLikeUrl =  host + '/author/' + post.author.url + '/inbox';
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

async function userLikesComment(postId, authorUrl) {
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
            const commentIdRegex = /comment(?:s)?\/([^\/]*)(?:\/)?(?:.*)$/g;
            let res = commentIdRegex.exec(likedEntityUrl);

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

async function getLikesComment(postId, commentId, authorUrl) {
    let url = authorUrl + "/post/" + postId + '/comments/' + commentId + '/likes';
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