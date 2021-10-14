import axios from "axios";
const baseUrl = "/api/author";

const register = async (username, password) => {
  axios.post(`${baseUrl}/register`, { username, password })
    .then((response) => {
      console.log(response)
      return true; 
    })
    .catch((error) => {
      console.log(error)
      return false;
    });
};

const login = async (username, password) => {
  axios.post(`${baseUrl}/login`, { username, password })
    .then((response) => {
      console.log(response)
      return true; 
    })
    .catch((error) => {
      console.log(error)
      return false;
    });
};

const authService = {
  login, register
};

export default authService;