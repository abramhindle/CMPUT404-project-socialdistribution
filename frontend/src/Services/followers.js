import { post, get, put, del } from "./requests";

export function getFollowers(authorID) {
    return get("authors/" + authorID + "/followers/");
}

export function addFollower(authorID, followerID) {
    console.log(authorID)
    console.log("authors/" + authorID + "/followers/" + followerID + "/")
    return put("authors/" + authorID + "/followers/" + followerID + "/", {});
}

export function deleteFollower(authorID, followerID) {
    return del(authorID + "followers/" + followerID + "/");
}