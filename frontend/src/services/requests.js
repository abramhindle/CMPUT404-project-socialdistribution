import axios from "axios";
import { useSelector, useDispatch } from 'react-redux';

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

export function post(path, data) {
    return axios.post(path, data, {headers: {"Authorization": "Token " + localStorage.getItem("token"), "X-CSRFToken": getCookie('csrftoken')}});
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