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

export function deleteRequest(params = {}) {
  const URL = `${domain}:${port}/delete-request/`;

  return axios
    .delete(URL, params, {
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


export function getRequest(params = {}) {
  const URL = `${params.authorID.toString()}/inbox-request/`;

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
