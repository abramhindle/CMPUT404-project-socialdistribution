import axios from "axios";
import { domain, port } from "./URL";

export function getFriendList(params = {}) {
  console.log("request freinds", params);
  const URL = `${params.authorID}/friends-list`;

  return axios
    .get(URL, {
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
