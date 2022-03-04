import { post, get, put, del } from "./requests";

export function getComments(authorID, postID) {
    return new Promise( (resolve, reject) => {
        const feedData=[
            {
                "type":"comment",
                "author":{
                    "type":"author",
                    "github": "http://github.com/gjohnson",
                    "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
                },
                "comment":"Sick Olde English",
                "contentType":"text",
                "published":"2015-03-09T13:07:04+00:00",
                "id":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/de305d54-75b4-431b-adb2-eb6b9e546013/comments/f6255bb01c648fe967714d52a89e8e9c",
            },
            {
                "type":"comment",
                "author":{
                    "type":"author",
                    "github": "http://github.com/gjohnson",
                    "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
                },
                "comment":"Sick Olde English",
                "contentType":"text/markdown",
                "published":"2015-03-09T13:07:04+00:00",
                "id":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/de305d54-75b4-431b-adb2-eb6b9e546013/comments/f6255bb01c648fe967714d52a89e8e9c",
            }
        ];
        resolve(feedData);
    } );
}




// export function getComments(authorID) {
//     return get(authorID + "inbox/");
// }

// export function createComments(data, userID){
//     return post(userID + "posts/", data);
// }

// export function editComments(data, cmID){
//     return put(cmID, data);
// }

// export function deleteComments(cmID){
//     return del(cmID);
// }

// export function getComments(data, authorID, postID, cmID){
//     const url = "authors/" + authorID + "/posts/" + postID + "/" + cmID +"/"
//     return get(url.replaceAll("/", "%2F"), data);
// }