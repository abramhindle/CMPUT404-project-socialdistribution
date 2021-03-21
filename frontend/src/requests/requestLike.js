import axios from "axios";

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

export function getInboxLikes (params = {}) {
    const URL = `${params.authorID.toString()}/inbox-like/`;
  
    return axios
      .get(URL, params, {
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

export function sendLikes(params = {}) {
    const URL =  `${params.postID}/likes/`
    const likesObject = {
        actor: params.actor,
        object: params.postID,
        summary: "I like you post!",
        context: "Post"
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