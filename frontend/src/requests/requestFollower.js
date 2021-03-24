import axios from "axios";

export function createFollower(params = {}) {
  const URL = params.object.toString() + "/followers/" + params.actor.toString() + "/";

  return axios
    .put(URL, params, {
      headers: {
        "Content-Type": "application/json",
        "Authorization": `JWT ${localStorage.getItem("token")}`,
      },
    })
    .then((response) => {
      return response;
    })
    .catch((error) => {
      return error.response;
    });
}

export function deleteFollower(params = {}) {
  const URL = params.object.toString() + "/followers/" + params.actor.toString();

  return axios
    .delete(URL, {
      headers: {
        "Content-Type": "application/json",
        "Authorization": `JWT ${localStorage.getItem("token")}`,
      },
    })
    .then((response) => {
      return response;
    })
    .catch((error) => {
      return error.response;
    });
}