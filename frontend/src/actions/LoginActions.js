import HTTPFetchUtil from "../util/HTTPFetchUtil";

export const sendLogin = (urlPath, requireAuth, body) => {

    return (dispatch, getstate) => {
        HTTPFetchUtil.sendPostRequest(urlPath, requireAuth, body)
            .then((results) => {

                const loginCredentials = {
                    username: body.username,
                    password: body.password,
                    userID: results.user.id
                }   
                console.log(loginCredentials, "hee heexd");

                return dispatch({
                    type: "SEND_LOGIN",
                    payload: loginCredentials
                })
            }).catch((error) => {
                console.error(error);
        })
    }
}