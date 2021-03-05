// evaluate action and send down certain state depending on action
import { GET_POST } from '../actions/types.js';

const initialState = {
    // user: {},
    // token: {}
}

export default function(state = initialState, action) {
    switch(action.type) {
        case GET_POST:
            return {
                ...state,
            };
        default:
            return state;
    }
}