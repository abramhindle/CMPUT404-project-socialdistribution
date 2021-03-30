import axios from "axios";

export function getLikes(params = {}) {
  const URL = `${params._object}/likes/`;

  return axios
    .get(URL, {
      headers: {
        "Content-Type": "application/json",
        Authorization: `JWT ${localStorage.getItem("token")}`,
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
        Authorization: `JWT ${localStorage.getItem("token")}`,
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
  const URL = `${params.postID}/likes/`;
  const likesObject = {
    actor: params.actor,
    object: params.object,
    summary: params.summary,
    context: params.postID,
  };

  return axios
    .post(URL, likesObject, {
      headers: {
        "Content-Type": "application/json",
        Authorization: `JWT ${localStorage.getItem("token")}`,
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
  const URL = `${params.postID}/liked/`;

  return axios
    .get(URL, {
      headers: {
        "Content-Type": "application/json",
        Authorization: `JWT ${localStorage.getItem("token")}`,
      },
    })
    .then((response) => {
      return response;
    })
    .catch((error) => {
      return error.response;
    });
}
//api
export function getRemoteLikes(params = {}) {
  return axios
    .get(params.URL, {
      headers: {
        "Content-Type": "application/json",
        Authorization: params.auth,
      },
    })
    .then((response) => {
      return response;
    })
    .catch((error) => {
      return error.response;
    });
}


export function sendRemoteLikes(params = {}) {
  const likesObject = {
    actor: params.actor,
    object: params.object,
    summary: params.summary,
    context: params.postID,
  };
  return axios
    .post(params.URL, likesObject, {
      headers: {
        "Content-Type": "application/json",
        Authorization: params.auth,
      },
    })
    .then((response) => {
      return response;
    })
    .catch((error) => {
      return error.response;
    });
}