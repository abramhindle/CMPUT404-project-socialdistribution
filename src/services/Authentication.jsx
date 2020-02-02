/* eslint-disable arrow-body-style */
import axios from "axios";

export const loginUser = (username, password) => {
  return axios.post("/auth/login/", {
    username,
    password,
  });
};

export const registerUser = (username, password) => {
  return axios.post("/auth/registration/", {
    username,
    password1: password,
    password2: password,
  });
};
