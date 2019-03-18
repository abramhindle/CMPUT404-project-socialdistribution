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
                            userID: results.authorId,
                            displayName: results.displayName,
                        }
                        
                        // Expiry time for cookie: 1/24 == 1 hour. 
      					Cookies.set("username", body.username, {expires: 1/24});
						Cookies.set("userID", results.authorId, {expires: 1/24});
						Cookies.set("displayName", results.displayName, {expires: 1/24});
						Cookies.set("userPass", window.btoa(body.username + ':' + body.password), 
						{expires: 1/24} );
                        

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