import axios from "axios";
import { domain, port } from "./URL";

export function getAllPublicPosts() {
  const URL = `${domain}:${port}/post-list/`;

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

export function getPostList(params = {}) {
  const URL = params.authorID.toString() + "/posts/";

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

export function getPost(params = {}) {
  const URL = params.postID;

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

export function sendPost(params = {}) {
  const URL = `${params.authorID.toString()}/posts/`;

  return axios
    .post(URL, params, {
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

export function updatePost(params = {}) {
  const URL = params.postID.toString() + "/";

  return axios
    .put(URL, params, {
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

export function deletePost(params = {}) {
  const URL = params.postID.toString() + "/";

  return axios
    .delete(URL, {
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

export function getInboxPost(params = {}) {
  const URL = params.authorID.toString() + "/inbox-post/";
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

// Remote API
export async function getAllRemotePublicPosts(params = {}) {
  // params = {URL: "", auth: "", ...}
  const body = {
    headers: {
      "Content-Type": "application/json",
      Authorization: params.auth,
    },
  };
  return axios
    .get(params.URL, body)
    .then((response) => {
      return response;
    })
    .catch((error) => {
      return error.response;
    });
}

export function sendPostToRemoteUser(params = {}) {
  const body = {
    headers: {
      "Content-Type": "application/json",
      Authorization: params.auth,
    },
  };
  return axios
    .post(params.URL, params.body, body)
    .then((response) => {
      return response;
    })
    .catch((error) => {
      return error.response;
    });
}