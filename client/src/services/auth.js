import axios from "axios";
const baseUrl = "/api/author";

const register = async (credentials) => {
  const response = await axios.post(`${baseUrl}/register`, new URLSearchParams(credentials));
  return response;
};

const login = async (credentials) => {
  const response = await axios.post(`${baseUrl}/login`, new URLSearchParams(credentials), { withCredentials: true, sameSite: "none" });
  return response;
};

const authService = {
  login, register
};

export default authService;