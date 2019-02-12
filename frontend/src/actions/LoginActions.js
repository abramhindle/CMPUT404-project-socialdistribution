import HTTPFetchUtil from "../util/HTTPFetchUtil";

export const sendLogin = (urlPath, requireAuth, body) => {

    return (dispatch, getstate) => {
        HTTPFetchUtil.sendPostRequest(urlPath, requireAuth, body)
            .then((results) => {
                return dispatch({
                    type: "SEND_LOGIN"
                })
            }).catch((error) => {
                console.error(error);
        })
    }
}