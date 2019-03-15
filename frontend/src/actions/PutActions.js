import HTTPFetchUtil from "../util/HTTPFetchUtil";

export const sendPut = (urlPath, requireAuth, body) => {

    return (dispatch, getstate) => {
        HTTPFetchUtil.sendPutRequest(urlPath, requireAuth, body)
            .then((httpResponse) => {
                if (httpResponse.status === 200) {
                	alert("Post edited successfully!");
                    httpResponse.json().then((results) => {
                        const putStatus = {status: 200,
                        }

                        return dispatch({
                            type: "SEND_PUT",
                            payload: putStatus
                        })
                    })
                }
                else {
                	alert("Failed to edit post");
                }
            })
            .catch((error) => {
                console.error(error);
        });
    }
}