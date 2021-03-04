import axios from "axios";
import { domain, port } from "./URL";

export function getCurrentUser(params = {}) {
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
    .catch((error) => {
      return error.response;
    });
}

export function handleLogout(params = {}) {
  localStorage.removeItem("token");
}
