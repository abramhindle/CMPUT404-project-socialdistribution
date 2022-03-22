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

export function getFollowing(authorID) {
    return get("authors/" + authorID + "/following/");
}

export function checkFollowing(authorID, followerID) {
    console.log("authors/" + authorID + "/following/" + followerID + "/");
    return get("authors/" + authorID + "/following/" + followerID + "/");
}

export function addFollowing(authorID, followerID) {
    return put("authors/" + authorID + "/following/" + followerID + "/", {});
}

export function deleteFollowing(authorID, followerID) {
    return del("authors/" + authorID + "/following/" + followerID + "/");
}