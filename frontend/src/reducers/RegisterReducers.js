const initialState = {
    isLoggedIn: false,
    userId: null,
    username: null,
    password: null
};

export default function registerReducers(state=initialState, action) {
    switch (action.type) {
        case "SEND_REGISTER":
            return Object.assign({}, state, {
                isLoggedIn: true,
                userId: action.payload.userID,
                username: action.payload.username,
                password: action.payload.password
                });
            default:
        return state;
    }
};
