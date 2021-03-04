import { message } from "antd";
import axios from "axios";
import { domain, port } from "./URL";

export function getPostList(params = {}) {
  const URL = params.authorID.toString() + '/posts/';

  return axios
    .get(URL, {
      headers: {
        "Content-Type": "application/json",
      },
    })
    .then((response) => {
      return response;
    })
    .catch((error) => message.error(error.response));
}

export function sendPost(params = {}) {
  const URL = `${params.authorID.toString()}/posts/`;

  return axios
    .post(URL, params, {
      headers: {
        "Content-Type": "application/json",
      },
    })
    .then((response) => {
      return response;
    })
    .catch((error) => message.error(error.response));
}
