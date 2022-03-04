import { post, get, put, del } from "./requests";

// export function getComments(authorID, postID) {
//     return new Promise( (resolve, reject) => {
//         const feedData=[
//             {
//                 "type":"comment",
//                 "author":{
//                     "type":"author",
//                     "github": "http://github.com/gjohnson",
//                     "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
//                 },
//                 "comment":"Sick Olde English",
//                 "contentType":"text",
//                 "published":"2015-03-09T13:07:04+00:00",
//                 "id":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/de305d54-75b4-431b-adb2-eb6b9e546013/comments/f6255bb01c648fe967714d52a89e8e9c",
//             },
//             {
//                 "type":"comment",
//                 "author":{
//                     "type":"author",
//                     "github": "http://github.com/gjohnson",
//                     "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
//                 },
//                 "comment":"Sick Olde English",
//                 "contentType":"text/markdown",
//                 "published":"2015-03-09T13:07:04+00:00",
//                 "id":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/de305d54-75b4-431b-adb2-eb6b9e546013/comments/f6255bb01c648fe967714d52a89e8e9c",
//             }
//         ];
//         resolve(feedData);
//     } );
// }


//  url = f"{settings.DOMAIN}/authors/{comment.post.author.local_id}/posts/{comment.post.local_id}/comments/{comment.id}"




// export function getInbox(authorID) {
//     return get(authorID + "inbox/");
// }

export function createComments(postData, userID, commentData){
    return post("authors/"+userID + "/posts/", postData, "/comments/", commentData);
}

export function editComments(cmID, userID, postData, commentData){
    return put("authors/"+userID + "/posts/", postData, "/comments/", commentData);
}

export function deleteComments(cmID, userID, postData){
    return del("authors/"+userID + "/posts/", postData, cmID);
}

export function getComments(postID){
    const url = postID + "comments"
    return get(url);
}

// export function getInbox(authorID) {
//     console.log("authors/" + authorID + "inbox/")
//     console.log(authorID)
//     return get("authors/" + authorID + "inbox/");
// }