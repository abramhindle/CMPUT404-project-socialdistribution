// evaluate action and send down certain state depending on action
import { GET_POST, POST_NEWPOST, GET_INBOX } from '../actions/types.js';

const initialState = {
    post: {},
    inbox: {}
}

export default function(state = initialState, action) {
    switch(action.type) {
        case GET_POST:
            return {
                ...state,
            };
        case POST_NEWPOST:
            return {
                ...state,
                post: action.payload
            };
        case GET_INBOX:
            return {
                ...state,
                inbox: action.payload
            }
        default:
            return state;
    }
}