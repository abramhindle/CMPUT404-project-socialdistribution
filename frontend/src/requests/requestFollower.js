import axios from "axios";
import { domain, port } from "./URL";

export function createFollower(params = {}) {
  const URL = params.object.toString() + "/followers/" + params.actor.toString() + "/";

  return axios
    .put(URL, params, {
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

export function deleteFollower(params = {}) {
  const URL = params.objectID.toString() + "/followers/" + params.actor.toString();

  return axios
    .delete(URL, {
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