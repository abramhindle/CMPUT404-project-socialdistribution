import HTTPFetchUtil from "../util/HTTPFetchUtil";

export const sendPost = (urlPath, requireAuth, body) => {

    return (dispatch, getstate) => {
        HTTPFetchUtil.sendPostRequest(urlPath, requireAuth, body)
            .then((httpResponse) => {
                if (httpResponse.status === 200) {
                	alert("Post made successfully!");
                    httpResponse.json().then((results) => {
                        const postStatus = {status: 200,
                        }

                        return dispatch({
                            type: "SEND_POST",
                            payload: postStatus
                        })
                    })
                }
                else {
                	alert("Failed to make post");
                }
            })
            .catch((error) => {
                console.error(error);
        });
    }
}