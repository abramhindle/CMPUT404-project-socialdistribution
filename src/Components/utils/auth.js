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

export async function setCurrentUser(user) {
	return localStorage.setItem("user", JSON.stringify(user));
}

export const unsetCurrentUser = () => {
	setAxiosAuthToken(null);
	localStorage.removeItem("token");
	localStorage.removeItem("user");
	localStorage.removeItem("loggedIn");
};

export async function getCurrentUser(author_id) {
	if (!localStorage.getItem("user")) {
		return await axios
			.get(`authors/${author_id}`)
			.then((response) => {
				const user = response.data;
				setCurrentUser(user);
			})
			.catch((res) => console.log(res));
	} else {
		return localStorage.getItem("user");
	}
}

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
	setToken(_csrfToken);
	return _csrfToken;
}

export function getAuthorId(a_id) {
	let author_id = "";
	const len = 36;
	if (a_id === null) {
		const author = JSON.parse(localStorage.getItem("user"));
		author_id = author.id.slice(author.id.length - len, author.id.length);
	} else {
		author_id = a_id.slice(a_id.length - len, a_id.length);
	}
	return author_id;
}

export const getProfileImageUrl = () => {
	const user = JSON.parse(localStorage.getItem("user"));
	return user.profileImage;
};
