import rp from "request-promise";
import store from "../store/index";

const getHeader = (requireAuth) => {
    if(requireAuth) {
        const loginCredentials = store.getState().loginReducers,
            username = loginCredentials.username,
            password = loginCredentials.password;

        return {"Content-Type": "application/json", 
                    'Authorization': 'Basic ' + 
                    window.btoa(username + ':' + password)};
    } else {
        return  {"Content-Type": "application/json"};
    }
}

const url = "http://localhost:8000"; //

export default class HTTPFetchUtil {

    /**
     * 
     * @param {String} path: the path we add to our host to send requests to. 
     * @param {Boolean} requireAuth: Whether we need to authenticate the requests or not to the backend 
     * @param {Object} requestBody: Content we want to add or change.
     */

    static sendPostRequest(path, requireAuth, requestBody) {
        const urlEndpoint = url.concat(path),
            bodyToSend = JSON.stringify(requestBody),
            headers = getHeader(requireAuth),
            payload = {
                method: "POST",
                body: bodyToSend,
                headers: headers
            },
            postRequest = new Request(urlEndpoint, payload);
        return fetch(postRequest)
        // const headerToSend = getHeader(requireAuth),
        //     endpoint = url.concat(path),
        //     storeValues = store.getState(),
        //     options = {
        //         method: "POST",
        //         uri: endpoint,
        //         headers: headerToSend,
        //         body: requestBody,
        //         json: true
        //     };

        // return rp.post(options);
    }
    /**
     * 
     * @param {String} path: the path we add to our host to send requests to. 
     * @param {Boolean} requireAuth: Whether we need to authenticate the requests or not to the backend 
     */

    static getRequest(path, requireAuth) {
        const urlEndpoint = url.concat(path),
            headers = getHeader(requireAuth),
            payload = {
                method: "GET",
                headers: headers
            },
            postRequest = new Request(urlEndpoint, payload);
        
        return fetch(postRequest)
        // const headerToSend = getHeader(requireAuth),
        //     endpoint = url.concat(path),
        //     options = {
        //         method: "GET",
        //         uri: endpoint,
        //         headers: headerToSend,
        //         json: true
        //     };

        // return rp.get(options);
    }
}
