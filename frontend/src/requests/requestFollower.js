import axios from "axios";

export function createFollower(params = {}) {
  const URL =
    params.object.toString() + "/followers/" + params.actor.toString() + "/";

  return axios
    .put(URL, params, {
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

export function getFollowerList(params = {}) {
  const URL = params.object.toString() + "/followers/";

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

export function getFollower(params = {}) {
  if (params.auth === undefined) {
    // if auth not given, consider as current server
    params.auth = `JWT ${localStorage.getItem("token")}`;
  }
  const URL =
    params.object.toString() + "/followers/" + params.actor.toString();
  return axios
    .get(URL, {
      headers: {
        "Content-Type": "application/json",
        Authorization: params.auth,
      },
      params: {
        remote: params.remote,
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
  const URL =
    params.object.toString() + "/followers/" + params.actor.toString();

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

// Remote API
export function createRemoteFollower(params = {}) {
  return axios
    .put(params.URL, params, {
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

export function deleteRemoteFollower(params = {}) {
  return axios
    .delete(params.URL, {
      headers: {
        "Content-Type": "application/json",
        Authorization: params.auth,
      },
      data: {
        remote: params.remote,
      },
    })
    .then((response) => {
      return response;
    })
    .catch((error) => {
      return error.response;
    });
}
