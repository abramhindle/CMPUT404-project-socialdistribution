const initialState = {
                        isLoggedIn: false,
                        userId: null,
                        username: null,
                        password: null
                    };

export default function loginReducers(state=initialState, action) {

    switch (action.type) {
        case "SEND_LOGIN":
            // console.log( ,"reducers");
            // return [state, action.sendLogin];
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
