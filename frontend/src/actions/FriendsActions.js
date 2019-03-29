import HTTPFetchUtil from "../util/HTTPFetchUtil";
export const getCurrentApprovedFriends = (urlPath, requireAuth, signal) => {
    return (dispatch) => {
        
        HTTPFetchUtil.getRequest(urlPath, requireAuth, signal)
            .then((httpResponse) => {
                if (httpResponse.status === 200) {
                    httpResponse.json().then((results) => { 
                        return dispatch({
                            type: "UPDATE_FRIENDS",
                            payload: results.friends,
                        })
                    })
                }
                else{
                    return httpResponse;
                }
            })
            .catch((error) => {
                console.error(error);
        });
    }
}

export const getCurrentFriendsRequests = (urlPath, requireAuth, signal) => {
    return (dispatch) => {
        HTTPFetchUtil.getRequest(urlPath, requireAuth, signal)
            .then((httpResponse) => {
                if (httpResponse.status === 200) {
                    httpResponse.json().then((results) => {
                        return dispatch({
                            type: "UPDATE_REQUESTS",
                            payload: results.authors,
                        })
                    })
                }
                else{
                    return httpResponse;
                }
            })
            .catch((error) => {
                console.error(error);
        });
    }
}