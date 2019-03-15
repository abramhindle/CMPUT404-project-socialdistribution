import HTTPFetchUtil from "../util/HTTPFetchUtil";

export const sendCurrentFriendsRequest = (urlPath, requireAuth) => {

    return (dispatch) => {
        
        HTTPFetchUtil.getRequest(urlPath, requireAuth)
            .then((httpResponse) => {
                if (httpResponse.status === 200) {
                    httpResponse.json().then((results) => { 
                        return dispatch({
                            type: "UPDATE_FRIENDS",
                            payload: results.friends,
                        })
                    })
                }
            })
            .catch((error) => {
                console.error(error);
        });
    }
}

export const sendPendingFriendsRequest = (urlPath, requireAuth) => {

    return (dispatch) => {
        HTTPFetchUtil.getRequest(urlPath, requireAuth)
            .then((httpResponse) => {
                if (httpResponse.status === 200) {
                    httpResponse.json().then((results) => {
                        return dispatch({
                            type: "UPDATE_REQUESTS",
                            payload: []//results.requests, //TODO: CURRENTLY ENDPOINT DOES NOT WORK
                        })
                    })
                }
            })
            .catch((error) => {
                console.error(error);
        });
    }
}