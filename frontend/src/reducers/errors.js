import {
    GET_ERRORS,
} from '../actions/types';

const initialState = {
    msg: {},
    status: null,
    origin: ''
}

export default function(state = initialState, action) {
    switch(action.type) {
        case GET_ERRORS:
            return {
                msg: action.payload.msg,
                status: action.payload.status,
                origin: action.payload.origin
            }
        default:
            return state;
    }
}