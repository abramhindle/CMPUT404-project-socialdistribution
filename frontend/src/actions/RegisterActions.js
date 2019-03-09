import HTTPFetchUtil from "../util/HTTPFetchUtil";

export const sendRegister = (urlPath, requireAuth, body) => {

    return (dispatch) => {
        HTTPFetchUtil.sendPostRequest(urlPath, requireAuth, body)
            .then((httpResponse) => {
                console.log(httpResponse);
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
                            isValid: body.isValid,
                        }

                        return dispatch({
                            type: "SEND_REGISTER",
                            payload: registerCredentials
                        })
                    })
                }
            })
            .catch((error) => {
                console.error(error);
        });
    }
}