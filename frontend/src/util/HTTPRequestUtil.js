import rp from "request-promise";

export default class RequestUtil {

    static postRequest(options) {

        return rp.post(options);
    }

    static getRequest(options) {

        return rp,get(options);
    }

    static putRequest(options) {

        return rp.put(options);
    }
}