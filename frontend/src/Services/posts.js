import { post, get, put, del } from "./requests";

export function getInbox(authorID) {
    return get(authorID + "inbox/");
}

export function createPost(data, userID){
    return post(userID + "posts/", data);
}

export function editPost(data, postID){
    return put(postID, data);
}

export function deletePost(postID){
    return del(postID);
}

export function getPost(data, authorID, postID){
    const url = "authors/" + authorID + "/posts/" + postID + "/"
    return get(url.replaceAll("/", "%2F"), data);
}