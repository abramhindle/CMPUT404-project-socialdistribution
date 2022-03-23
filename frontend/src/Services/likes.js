import { post, get, put, del, patch } from "./requests";



export function createCommentLikes(commentData, likesData){
    console.log(commentData.id + "likes/", likesData)
    return post(commentData.id + "likes/", likesData);
}

export function getCommentLikes(commentData){
    return get(commentData.id + "likes/");
}

export function deleteCommentLikes(commentData, likesData){
    return post(commentData.id + "likes/decrement/", likesData);
}

export function createLikes(postData, likesData){
    return post(postData.id + "likes/", likesData);
}

export function deleteLikes(postData, likesData){
    return post(postData.id + "likes/decrement/", likesData);
}

export function getLikes(postData){
    return get(postData.id + "likes/");
}

export function getAllLikes(author){
    console.log(author.url + "liked/");
    return get(author.url + "liked/");
}
