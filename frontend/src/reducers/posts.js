// evaluate action and send down certain state depending on action
import { GET_POST, POST_NEWPOST } from '../actions/types.js';

const initialState = {
    post: {}
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
        default:
            return state;
    }
}