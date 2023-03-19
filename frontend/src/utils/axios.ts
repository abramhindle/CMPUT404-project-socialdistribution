import axios from "axios";

// export const fe_uname = process.env['FE_UNAME'];     FIXME: Couldn't figure out how to load env variables
// export const fe_pw = process.env['FE_PW'];

const instance = axios.create({
    baseURL: "http://localhost:8000/service",       // CHANGED: "/services" to "/service"
    auth: {
        username: "admin",      // FIXME: This is wrong in so many ways but idk how else to do it so...
        password: "123"
    },
    headers: {
        "Content-Type": "application/json",
    }
});

export default instance;