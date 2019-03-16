import HTTPFetchUtil from "../util/HTTPFetchUtil";
import Cookies from 'js-cookie';

export const sendLogin = (urlPath, requireAuth, body) => {

    return (dispatch, getstate) => {
        HTTPFetchUtil.sendPostRequest(urlPath, requireAuth, body)
            .then((httpResponse) => {
                if (httpResponse.status === 200) {
                    httpResponse.json().then((results) => { 
                        const loginCredentials = {
                            username: body.username,
                            password: body.password,
                            userID: results
                        }
      					Cookies.set("username", body.username, {expires: 1/96});
						Cookies.set("userID", results, {expires: 1/96});
						Cookies.set("userPass", window.btoa(body.username + ':' + body.password), 
						{expires: 1/96} );
                        

                        return dispatch({
                            type: "SEND_LOGIN",
                            payload: loginCredentials
                        })
                    })
                }
            })
            .catch((error) => {
                console.error(error);
        });
    }
}