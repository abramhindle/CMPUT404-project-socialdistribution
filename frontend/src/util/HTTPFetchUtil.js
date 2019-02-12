import rp from "request-promise";

const getHeader = (requireAuth) => {
    
    if(requireAuth) {
        return {"Content-Type": "application/json", 'Authorization': 'Basic ' + window.btoa("test1" + ':' + "test1")};
    } else {
        return  {"Content-Type": "application/json"};
    }
}

const url = "http://localhost:8000"; //

export default class HTTPFetchUtil {

    static sendPostRequest(path, requireAuth, requestBody) {

        const headerToSend = getHeader(requireAuth),
            endpoint = url.concat(path);
        const options = {
            method: "POST",
            uri: endpoint,
            headers: headerToSend,
            body: requestBody,
            json: true
        };

        return rp.post(options);
    }

    static getRequest(path, requireAuth, requestBody) {


        // return rp.get(options);
    }
}
