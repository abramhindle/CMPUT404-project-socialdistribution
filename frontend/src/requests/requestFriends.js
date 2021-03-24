import axios from "axios";

export function getFriendList(params = {}) {
  const URL = `${params.authorID}/friends-list/`;

  return axios
    .get(URL, {
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
