import { post, get, put, del, patch } from "./requests";



export function createCommentLikes(commentData, likesData){
    console.log(commentData.id + "likes/", likesData)
    return post(commentData.id + "likes/", likesData);
}

export function getCommentLikes(commentData){
    // console.log(postData.id + "likes/");
    return get(commentData.id + "likes/");
}

export function deleteCommentLikes(commentData, likesData){
    return post(commentData.id + "likes/decrement/", likesData);
}

export function createLikes(postData, likesData){
    // console.log(postData.id + "likes/", likesData)
    return post(postData.id + "likes/", likesData);
}

export function deleteLikes(postData, likesData){
    return post(postData.id + "likes/decrement/", likesData);
}

export function getLikes(postData){
    // console.log(postData.id + "likes/");
    return get(postData.id + "likes/");
}

export function getAllLikes(author){
    console.log(author.url + "liked/");
    return get(author.url + "liked/");
}
