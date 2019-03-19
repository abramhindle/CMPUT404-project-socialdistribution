import utils from "../util/utils";

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
        console.log(action.payload)
            return Object.assign({}, state, {
                isLoggedIn: true,
                userId: action.payload.userID,
                username: action.payload.username,
                password: action.payload.password,
                hostName: utils.getHostName(action.payload.userID),
                authorId: utils.getShortAuthorId(action.payload.userID),
                displayName: action.payload.displayName
              });
        default:
            return state;
    }
};
