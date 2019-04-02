import HTTPFetchUtil from "../util/HTTPFetchUtil";
import Cookies from 'js-cookie';

export const sendLogin = (urlPath, requireAuth, body, signal) => {

    return (dispatch, getstate) => {
        HTTPFetchUtil.sendPostRequest(urlPath, requireAuth, body, signal)
            .then((httpResponse) => {
                if (httpResponse.status === 200) {
                    httpResponse.json().then((results) => { 
                        const loginCredentials = {
                            username: body.username,
                            password: body.password,
                            userID: results.authorId,
                            displayName: results.displayName,
                        }
                        
                        // Expiry time for cookie: 1 == 1 day. 
      					Cookies.set("username", body.username, {expires: 1});
						Cookies.set("userID", results.authorId, {expires: 1});
						Cookies.set("displayName", results.displayName, {expires: 1});
						Cookies.set("userPass", window.btoa(body.username + ':' + body.password), 
						{expires: 1} );
                        

                        return dispatch({
                            type: "SEND_LOGIN",
                            payload: loginCredentials
                        })
                    })
                }
                else {
                	return dispatch({
                		type: "FAILED_LOGIN",
                	})
                }
            })
            .catch((error) => {
                console.error(error);
        });
    }
}

export const sendLogout = () => {
    return (dispatch) => {
        return dispatch({
            type: "SEND_LOGOUT"
        })
    }
}
