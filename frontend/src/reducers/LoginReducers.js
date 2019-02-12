const initialState = {
                        isLoggedIn: false,
                        userId: null,
                        username: null,
                        password: null
                    };

export default function loginReducers(state=initialState, action) {

    switch (action.type) {
        case "SEND_LOGIN":
            console.log(action, "reducers");
            // return [state, action.sendLogin];
            return Object.assign({}, state, {
                isLoggedIn: true,
                userId: null,
                username: null,
                password: null
              });
        default:

            return state;
    }
};
