import axios from "axios";
import { domain, port } from "./URL";


export function postRequest(params = {}) {
  const URL = `${domain}:${port}/friend-request/`;

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
