const initialState = {
    friends: null,
    requests: null,
};

export default function friendsReducer(state=initialState, action) {
    switch (action.type) {
        case "UPDATE_FRIENDS":
            return Object.assign({}, state, {
                friends: action.payload
            });
        case "UPDATE_REQUESTS":
            return Object.assign({}, state, {
                requests: action.payload//TODO: NOT CORRECT PAYLOAD OBJECT
            });
        default:
            return state;
    }
};
