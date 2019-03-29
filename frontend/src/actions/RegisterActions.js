import HTTPFetchUtil from "../util/HTTPFetchUtil";

export const sendRegister = (urlPath, requireAuth, body, signal) => {

    return (dispatch) => {
        HTTPFetchUtil.sendPostRequest(urlPath, requireAuth, body, signal)
            .then((httpResponse) => {
                if (httpResponse.status === 200) {
                    httpResponse.json().then((results) => {
                        const registerCredentials = {
                            username: body.username,
                            password: body.password,
                            firstName: body.firstName,
                            lastName: body.lastName,
                            displayName: body.displayName,
                            email: body.email,
                            github: body.github,
                            bio: body.bio,
                        }

                        return dispatch({
                            type: "SEND_REGISTER",
                            payload: registerCredentials
                        })
                    })
                }
                else {
                	return dispatch({
                		type: "FAILED_REGISTER",
                	})
                }
            })
            .catch((error) => {
                console.error(error);
        });
    }
}

export const resetRegister = () => {
    return (dispatch) => {
        return dispatch({
            type: "RESET_REGISTER"
        })
    }
}