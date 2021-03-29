import axios from "axios";
import { domain, port } from "./URL";

export function postRequest(params = {}) {
  const URL = `${domain}:${port}/friend-request/`;

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

export function deleteRequest(params = {}) {
  const URL = params.object.toString() + "/request/" + params.actor.toString();

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

export function getRequest(params = {}) {
  const URL = `${params.authorID.toString()}/inbox-request/`;
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
export function postRemoteRequest(params = {}) {
  return axios
    .post(params.URL, params, {
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

export function deleteRemoteRequest(params = {}) {
  return axios
    .delete(params.URL, {
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

export function getRemoteRequest(params = {}) {
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