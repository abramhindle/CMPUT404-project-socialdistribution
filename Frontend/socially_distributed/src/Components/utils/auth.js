import axios from "axios";

export const setAxiosAuthToken = (token) => {
	if (typeof token !== "undefined" && token) {
		//Apply the TOKEN for every request that we will make in the future.
		axios.defaults.headers.common["Authorization"] = "Token " + token;
	} else {
		//Delete auth header
		delete axios.defaults.headers.common["Authorization"];
	}
};

export const setLoggedIn = (bool) => {
	localStorage.setItem("loggedIn", bool);
};

export const setToken = (token) => {
	localStorage.setItem("token", token);
};

export const setCurrentUser = (user) => {
	localStorage.setItem("user", JSON.stringify(user));
};

export const unsetCurrentUser = () => {
	setAxiosAuthToken(null);
	localStorage.removeItem("token");
	localStorage.removeItem("user");
	localStorage.removeItem("loggedIn");
};

export const getCurrentUser = (author_id) => {
	axios.get("authors/authors/" + author_id).then((response) => {
		console.log(response.data);
		const user = response.data;
		console.log(user);
		setCurrentUser(user);
	});
};

export async function getCsrfToken() {
	let _csrfToken = null;
	const API_HOST = "http://localhost:8000";
	if (_csrfToken === null) {
		const response = await fetch(`${API_HOST}/csrf/`, {
			credentials: "include",
		});
		const data = await response.json();
		_csrfToken = data.csrfToken;
	}
	console.log(_csrfToken);
	setToken(_csrfToken);
	return _csrfToken;
}
