// evaluate action and send down certain state depending on action
import { POST_NEWPOST } from '../actions/types.js';

const initialState = {
    post: {}
}

export default function(state = initialState, action) {
    switch(action.type) {
        case POST_NEWPOST:
            return {
                ...state,
                post: action.payload
            };
        default:
            return state;
    }
}