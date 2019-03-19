const initialState = {
                        isLoggedIn: false,
                        userId: null,
                        username: null,
                        password: null,
                        authorId: null,
                        hostName: null,
                    };

export default function loginReducers(state=initialState, action) {
    switch (action.type) {
        case "SEND_LOGIN":
            return Object.assign({}, state, {
                isLoggedIn: true,
                userId: action.payload.userId,
                username: action.payload.username,
                password: action.payload.password,
                hostName: action.payload.hostName,
                authorId: action.payload.authorId,
                displayName: action.payload.displayName
              });
        default:
            return state;
    }
};
