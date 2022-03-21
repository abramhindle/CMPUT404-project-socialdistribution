import { post, get, put, del, patch } from "./requests";

export function pushToInbox(authorID, data){
    return post("authors/" + authorID + "/inbox/", data);
}

export function getInbox(authorID) {
    return get("authors/" + authorID + "/inbox/");
}
