// evaluate action and send down certain state depending on action
import { POST_LOGIN, POST_REGISTER, POST_SEARCH_DISPLAYNAME, POST_FRIEND_REQUEST, GET_GITHUB } from '../actions/types.js';

const initialState = {
    user: {},
    displayNameSearchResult: [],
    friendRequest: {},
    github_activity: []
}

export default function(state = initialState, action) {
    switch(action.type) {
        case POST_REGISTER:
            return {
                ...state,
                user: action.payload
            };
        case POST_LOGIN:
            return {
                ...state,
                user: action.payload
            };
        case POST_SEARCH_DISPLAYNAME:
            return {
                ...state,
                displayNameSearchResult: action.payload
            }
        case POST_FRIEND_REQUEST:
            return {
                ...state,
                friendRequest: action.payload
            }
        case GET_GITHUB:
            return {
                ...state,
                github_activity: action.payload
            }
        default:
            return state;
    }
}