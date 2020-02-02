import axios from "axios";

export const loginUser = (username, password) => {
    return axios.post("/auth/login/", {
        username: username,
        password: password,
    });
}

export const registerUser = (username, password) => {
    return axios.post("/auth/registration/", {
        username: username,
        password1: password,
        password2: password,
    });
}
