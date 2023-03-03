import axios from "axios";

const instance = axios.create({
    baseURL: "http://localhost:8000/services",
    headers: {
        "Content-Type": "application/json",
    }
});

export default instance;