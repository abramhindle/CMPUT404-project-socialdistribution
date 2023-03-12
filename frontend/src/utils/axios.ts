import axios from "axios";

const instance = axios.create({
    baseURL: "http://localhost:8000/service",       // CHANGED: "/services" to "/service"
    headers: {
        "Content-Type": "application/json",
    }
});

export default instance;