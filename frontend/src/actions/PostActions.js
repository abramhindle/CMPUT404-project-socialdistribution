import HTTPFetchUtil from "../util/HTTPFetchUtil";

export const sendPost = (urlPath, requireAuth, body) => {

	console.log(body);
    return (dispatch, getstate) => {
        HTTPFetchUtil.sendPostRequest(urlPath, requireAuth, body)
            .then((httpResponse) => {
                console.log(httpResponse);
                if (httpResponse.status === 200) {
                    httpResponse.json().then((results) => {
                        const postStatus = {status: 200,
                        }

                        return dispatch({
                            type: "SEND_POST",
                            payload: postStatus
                        })
                    })
                }
            })
            .catch((error) => {
                console.error(error);
        });
    }
}