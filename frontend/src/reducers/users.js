// evaluate action and send down certain state depending on action
import { POST_LOGIN, POST_REGISTER, POST_SEARCH_DISPLAYNAME } from '../actions/types.js';

const initialState = {
    user: {},
    displayNameSearchResult: []
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
        default:
            return state;
    }
}