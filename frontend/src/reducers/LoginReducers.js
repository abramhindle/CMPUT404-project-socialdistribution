const initialState = {
                        isLoggedIn: false,
                        userId: null,
                        username: null,
                        password: null
                    };

export default function loginReducers(state=initialState, action) {
    switch (action.type) {
        case "SEND_LOGIN":
            return Object.assign({}, state, {
                isLoggedIn: true,
                userId: action.payload.userID,
                username: action.payload.username,
                password: action.payload.password,
                displayName: action.payload.displayName
              });
         case "SEND_LOGOUT":
            return Object.assign({}, state, initialState);
        default:
            return state;
    }
};
