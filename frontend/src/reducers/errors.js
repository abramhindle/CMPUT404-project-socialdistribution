import {
    GET_ERRORS,
    GET_SUCCESS
} from '../actions/types';

const initialState = {
    msg: {},
    status: null,
    origin: '',
}

export default function(state = initialState, action) {
    switch(action.type) {
        case GET_ERRORS:
            return {
                msg: action.payload.msg,
                status: action.payload.status,
                origin: action.payload.origin
            }
        case GET_SUCCESS:
            return {
                origin: action.payload.origin,
                status: action.payload.status
            }
        default:
            return state;
    }
}