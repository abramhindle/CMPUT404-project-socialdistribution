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
