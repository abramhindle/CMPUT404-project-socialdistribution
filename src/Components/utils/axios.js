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
	},
	auth: {
		username: username,
		password: password,
	},
});
