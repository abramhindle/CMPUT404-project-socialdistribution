import { post, get, put, del, patch } from "./requests";


export function createLikes(postData, likesData){
    console.log(postData.id + "likes/", likesData)
    return post(postData.id + "likes/", likesData);
}


export function createCommentLikes(commentData){
    console.log(commentData.id + "likes/")
    // return post(postData.id + "comments/", commentData);
}

export function deleteLikes(postData){
    return del(postData.id + "likes/");
}

export function getLikes(postData){
    console.log(postData.id + "likes/");
    return get(postData.id + "likes/");
}
