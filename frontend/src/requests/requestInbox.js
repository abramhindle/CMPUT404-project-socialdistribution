import axios from "axios";

export function sendToInbox(params = {}) {
  const URL = `${params.authorID}/inbox/`;
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

export function sendToRemoteInbox(params = {}) {
  const URL = `${params.authorID}/inbox/`;
  return axios
    .post(URL, params, {
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

export function clearInbox(params = {}) {
  const URL = `${params.authorID}/inbox/`;
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
