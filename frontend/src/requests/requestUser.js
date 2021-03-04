import { message } from "antd";
import axios from "axios";
import { domain, port } from "./URL";

export function getPostList(params = {}) {
  const URL = `${domain}:${port}/current_user/`;

  return axios
    .get(URL, {
      headers: {
        Authorization: `JWT ${localStorage.getItem("token")}`,
      },
    })
    .then((response) => {
      return response;
    })
    .catch((error) => message.error(error.response));
}

export function handleLogin(params = {}) {
  const URL = `${domain}:${port}/token-auth/`;

  return axios
    .post(URL, params, {
      headers: {
        "Content-Type": "application/json",
      },
    })
    .then((response) => {
      console.log("handle login", response);
      localStorage.setItem("token", response.token);
      return response;
    })
    .catch((error) => message.error(error.response));
}

export function handleLogout(params = {}) {
  localStorage.removeItem("token");
}
