import { post, get, put, del, patch } from "./requests";

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

export function createComment(postData, commentData){
    console.log(postData.id + "comments/")
    return post(postData.id + "comments/", commentData);
}

export function editComment(oldComment, content){
    return patch(oldComment.id, content);
}

export function deleteComment(comment){
    return del(comment.id);
}

export function getComments(postID){
    return get(postID + "comments/");
}

// export function getInbox(authorID) {
//     console.log("authors/" + authorID + "inbox/")
//     console.log(authorID)
//     return get("authors/" + authorID + "inbox/");
// }