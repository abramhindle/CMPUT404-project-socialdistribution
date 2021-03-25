import axios from "axios";
import { domain, port } from "./URL";

export function getLikes(params = {}) {
  const URL = `${params._object}/likes/`;

  return axios
    .get(URL, {
      headers: {
        "Content-Type": "application/json",
      },
    })
    .then((response) => {
      return response;
    })
    .catch((error) => {
      return error.response;
    });
}

export function getinboxlike(params = {}) {
    const URL = `${params.authorID.toString()}/inbox-like/`;
    return axios
    .get(URL, {
      headers: {
        "Content-Type": "application/json",
        "Authorization": `JWT ${localStorage.getItem("token")}`,
      },
    })
    .then((response) => {
      return response;
    })
    .catch((error) => {
      return error.response;
    });
}

export function sendLikes(params = {}) {
    const URL =  `${params.postID}/likes/`
    const likesObject = {
        actor: params.actor,
        object: params.postID,
        summary: "I like you post!",
        context: params.postID
    };
  
    return axios
      .post(URL, likesObject, {
        headers: {
          "Content-Type": "application/json",
        },
      })
      .then((response) => {
        return response;
      })
      .catch((error) => {
        return error.response;
      });
}

export function getLiked(params = {}) {
    const URL = `${params.postID}/liked/`
  
    return axios
      .get(URL, {
        headers: {
          "Content-Type": "application/json",
        },
      })
      .then((response) => {
        return response;
      })
      .catch((error) => {
        return error.response;
      });
  }