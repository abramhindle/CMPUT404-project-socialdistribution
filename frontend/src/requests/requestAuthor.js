import { message } from "antd";
import axios from "axios";
import { domain, port } from "./URL";

export function getAuthor(params = {}) {
  const URL = params.authorID.toString();

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

export function postAuthor(params = {}) {
  const URL = `${domain}:${port}/author/`;
  const requestBody = {
    displayName: params.displayName,
    github: params.github,
    username: params.userName,
    email: params.email,
    password: params.password,
  };

  return axios
    .post(URL, requestBody, {
      headers: {
        "Content-Type": "application/json",
      },
    })
    .then((response) => {
      return response;
    })
    .catch((error) => message.error(error.response));
}
