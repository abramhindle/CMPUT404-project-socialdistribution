import { post, get, put, del, patch } from "./requests";


export function createCommentLikes(commentData, sender){
    const data = {
        "summary": `${sender.displayName} Likes Your Comment!`,         
        "type": "Like",
        "author": sender,    
        "object": commentData.id
    }
    return post("authors/" + commentData.author.id + "/inbox/", data);
}

export function getCommentLikes(commentData){
    return get(commentData.id + "likes/");
}

export function deleteCommentLikes(commentData, likesData){
    return post(commentData.id + "likes/decrement/", likesData);
}

export function createPostLikes(postData, sender){
    const data = {
        "summary": `${sender.displayName} Likes Your Post!`,         
        "type": "Like",
        "author": sender,    
        "object": postData.id
    }
    return post("authors/" + postData.author.id + "/inbox/", data);
}

export function deleteLikes(postData, likesData){
    return post(postData.id + "likes/decrement/", likesData);
}

export function getLikes(postData){
    return get(postData.id + "likes/");
}

export function getAllLikes(author){
    return get(author.url + "liked/");
}
