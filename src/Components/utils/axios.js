import axios from "axios";
import { getCsrfToken } from "./auth";

var username = localStorage.getItem("username");
var password = localStorage.getItem("password");

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
