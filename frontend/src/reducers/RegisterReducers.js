const initialState = {
    isLoggedIn: false,
    registerFailure: false,
    userId: null,
    username: null,
    password: null
};

export default function registerReducers(state=initialState, action) {
    switch (action.type) {
        case "SEND_REGISTER":
            return Object.assign({}, state, {
                isLoggedIn: true,
                registerFailure: false,
                userId: action.payload.userID,
                username: action.payload.username,
                password: action.payload.password
                });
                
        case "FAILED_REGISTER":
        	return Object.assign({}, state, {
        		registerFailure: true,
        	});
        
        case "RESET_REGISTER":
        	return Object.assign({}, state, initialState);
        default:
    		return state;
    }
};
