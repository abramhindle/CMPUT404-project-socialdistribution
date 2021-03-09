import axios from "axios";
import { domain, port } from "./URL";

export function getCommentList(params = {}) {
  const URL = `${params.postID.toString()}/comments/`;

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

export function getComment(params = {}) {
  const URL = params.commentID.toString() + '/';

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

export function postComment(params = {}) {
  const URL = `${params.postID.toString()}/comments/`;

  return axios
    .post(URL, params, {
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
