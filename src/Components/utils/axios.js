import axios from "axios";
import { getCsrfToken } from "./auth";

var username = localStorage.getItem("username");
var password = localStorage.getItem("password");
var base64encodedData = username + ":" + password;
var base64String = btoa(base64encodedData);
getCsrfToken();
var token = localStorage.getItem("token");
export let reqInstance = axios.create({
	headers: {
		"X-CSRFToken": token,
		Authorization: "Basic " + base64String,
	},
	baseURL: `http://${username}:${password}@127.0.0.1:8000/`,
	auth: {
		username: username,
		password: password,
	},
});
