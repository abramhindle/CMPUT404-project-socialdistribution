import axios from "axios";

// export const fe_uname = process.env['FE_UNAME'];     FIXME: Couldn't figure out how to load env variables
// export const fe_pw = process.env['FE_PW'];

const instance = axios.create({
    baseURL: "http://localhost:8000/service",       // CHANGED: "/services" to "/service"
    auth: {
        username: "admin", //process.env.FE_UNAME || "default",      // FIXME: This is wrong in so many ways but idk how else to do it so...
        password: "123" //process.env.FE_PW || "default"
    },
    headers: {
        "Content-Type": "application/json",
    }
});

export const remoteInstance = axios.create({
    baseURL: "https://sd7-api.herokuapp.com/api",       // CHANGED: "/services" to "/service"
    auth: {
        username: "node01", //process.env.FE_UNAME || "default",      // FIXME: This is wrong in so many ways but idk how else to do it so...
        password: "P*ssw0rd!" //process.env.FE_PW || "default"
    },
    headers: {
        "Content-Type": "application/json",
    }
});

export default instance;