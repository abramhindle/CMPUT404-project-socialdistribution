$(document).ready(function() {
    posts = document.querySelectorAll('div.post')

    posts.forEach((post) => {
        let postId = post.getAttribute("post-id");
        let authorOfPostId = post.getAttribute("author-id");
        let userAuthorId = user_author;

        let likeButton = document.getElementById(postId + '-like-button');
        likeButton.onclick = async function() {
            if (user_authenticated == "True") {                
                await likePost(postId, authorOfPostId, userAuthorId);

                // update with actual user
                await updateLikedPost(postId, userAuthorId);

            } else {
                alert("You need to Log In");
            }   
        };

        updateLikedPost(postId, userAuthorId);
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
            'X-CSRFToken' : "{{ csrf_token }}"
    },})
    .then(function(authorResponse) {
        return authorResponse.json();
    })
    .then(async function(authorLikingPost) {
        console.log(authorLikingPost);

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
        })
        // TODO remove
        .then(function(){
            alert("Like created!");

        });
    })
    
    
}

async function updateLikedPost(postId, authorOfPostId) {
    let userAuthorUrl = host + '/author/' + authorOfPostId
    await checkLikedClassPost(postId, userAuthorUrl);
}

async function checkLikedClassPost(postId, userAuthorUrl) {
    let likeButton = document.getElementById(postId + '-like-button');
    let likesPost = await userLikesPost(postId, userAuthorUrl)
    if (likesPost) {
        likeButton.classList.remove("liked");
        likeButton.classList.add("liked");
    }
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