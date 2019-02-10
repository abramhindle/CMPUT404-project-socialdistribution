import rp from "request-promise";

const getHeader = (requireAuth) => {
    
    if(requireAuth) {
        return {"Content-Type": "application/json", 'Authorization': 'Basic ' + window.btoa("test1" + ':' + "test1")};
    } else {
        return  {"Content-Type": "application/json"};
    }
}

export default class HTTPFetchUtil {

    static sendPostRequest() {
        const options = {
            method: "POST",
            uri: "http://localhost:8000/api/profile/",
            headers: {
                        "Content-Type": "application/json",
                        'Authorization': 'Basic ' + window.btoa("test1" + ':' + "test1").toString('base64')},
            body: {
                github: "derricks numbani github"
            }
        }

        return rp.post(options);
    }

    // static sendPostRequest(){
    //     let headers = {"Content-Type": "application/json", 'Authorization': 'Basic ' + window.btoa("test1" + ':' + "test1")};
    //     let body = JSON.stringify({github: "derricks numbani github"});
    //     return fetch("/api/profile/", {headers, body, method: "POST"})
            
    // }
    
    // static sendPostRequest(body, requireAuth, endpointURL) {
    //     const requestBody = JSON.stringify(body),
    //         headers = getHeader(requireAuth);

    //     const testheader = {"Content-Type": "application/json", 'Credentials': 'include', 'Authorization': 'Basic ' + window.btoa("test1" + ':' + "test1")};
    //     console.log(headers, "test 1");
    //     console.log(testheader, "test 2");
    //     const testbody = JSON.stringify({github: "derricks numbani github"});
    //     return fetch("/api/profile/", {testheader, testbody, method: "POST"})
    //         .then((results) => {
    //             console.log(results, "save me");
    //         });
    // }



    // static getRequest(options) {

    //     return rp,get(options);
    // }

    // static putRequest(options) {

    //     return rp.put(options);
    // }
}