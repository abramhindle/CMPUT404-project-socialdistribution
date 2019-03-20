const initialState = {
    friends: [],
    requests: [],
};

export default function friendsReducer(state=initialState, action) {
    switch (action.type) {
        case "UPDATE_FRIENDS":
            return Object.assign({}, state, {
                friends: action.payload
            });
        case "UPDATE_REQUESTS":
            return Object.assign({}, state, {
                requests: action.payload
            });
        default:
            return state;
    }
};
