import { post, get, put, del } from "./requests";

export function getNotifications(authorID) {
    const localID = authorID.split("/")[authorID.split("/").length - 2];
    return get("api/authors/" + localID + "/notifications/");
}

export function deleteNotification(authorID, notificationID) {
    const localID = authorID.split("/")[authorID.split("/").length - 2];
    return del("api/authors/" + localID + "/notifications/" + notificationID);
}

// export function getNotifications(authorID) {
//     const localID = authorID.split("/")[authorID.split("/").length - 2];
//     return get("api/authors/" + localID + "/notifications/");
// }