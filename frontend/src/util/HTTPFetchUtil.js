//import store from "../store/index";
import Cookies from 'js-cookie';

const getHeader = (requireAuth) => {
    if(requireAuth) {
        return {"Content-Type": "application/json", 
                    'Authorization': 'Basic ' + 
                    Cookies.get('userPass')};
    } else {
        return  {"Content-Type": "application/json"};
    }
}

const PROD_URL = "https://radiant-savannah-77591.herokuapp.com",
     LOCALHOST = "http://localhost:8000",
     url = (window.location.hostname === "localhost" ? LOCALHOST : PROD_URL);

export default class HTTPFetchUtil {

    /**
     * 
     * @param {String} path: the path we add to our host to send requests to. 
     * @param {Boolean} requireAuth: Whether we need to authenticate the requests or not to the backend 
     * @param {Object} requestBody: Content we want to add or change.
     */

    static sendPostRequest(path, requireAuth, requestBody, signal) {
        const urlEndpoint = url.concat(path),
            bodyToSend = JSON.stringify(requestBody),
            headers = getHeader(requireAuth),
            payload = {
                method: "POST",
                body: bodyToSend,
                headers: headers
            },
            postRequest = new Request(urlEndpoint, payload);
        return fetch(postRequest, signal)
    }
    
    static sendPutRequest(path, requireAuth, requestBody, signal) {
        const urlEndpoint = url.concat(path),
            bodyToSend = JSON.stringify(requestBody),
            headers = getHeader(requireAuth),
            payload = {
                method: "PUT",
                body: bodyToSend,
                headers: headers
            },
            putRequest = new Request(urlEndpoint, payload);
        return fetch(putRequest, signal)
    }
    
    /**
     * 
     * @param {String} path: the path we add to our host to send requests to. 
     * @param {Boolean} requireAuth: Whether we need to authenticate the requests or not to the backend 
     */

    static getRequest(path, requireAuth, signal) {
        const urlEndpoint = url.concat(path),
            headers = getHeader(requireAuth),
            payload = {
                method: "GET",
                headers: headers
            },
            getRequest = new Request(urlEndpoint, payload);
        
        return fetch(getRequest, signal)
    }
    
    static deleteRequest(path, requireAuth, signal) {
		const urlEndpoint = url.concat(path),
			headers = getHeader(requireAuth),
			payload = {
			method: "DELETE",
                headers: headers
            },
            deleteRequest = new Request(urlEndpoint, payload);
        return fetch(deleteRequest, signal)
    }
}
