import axios from "axios";

export function post(path, data) {
    return axios.post(path, data, {headers: {"Authorization": "Token " + localStorage.getItem("token")}});
}

export function put(path, data) {
    return axios.put(path, data, {headers: {"Authorization": "Token " + localStorage.getItem("token")}});
}

export function patch(path, data) {
    return axios.patch(path, data, {headers: {"Authorization": "Token " + localStorage.getItem("token")}});
}

export function get(path) {
    return axios.get(path, {headers: {"Authorization": "Token " + localStorage.getItem("token")}});
}

export function del(path) {
    return axios.delete(path, {headers: {"Authorization": "Token " + localStorage.getItem("token")}});
}