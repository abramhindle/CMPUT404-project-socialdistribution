import { post, get, put, del, patch } from "./requests";


export function createComment(postData, commentData){
    console.log(postData.id + "comments/")
    return post("authors/" + postData.author.id + "posts/" + postData.id + "/comments/", commentData);
}

export function editComment(oldComment, content){
    return patch(oldComment.id, content);
}

export function deleteComment(comment){
    return del(comment.id);
}

export function getComments(postData){
    return get("authors/" + postData.author.id + "posts/" + postData.id + "/comments/");
}

