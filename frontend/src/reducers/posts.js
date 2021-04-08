// evaluate action and send down certain state depending on action
import {
    GET_POST,
    POST_NEWPOST,
    GET_INBOX,
    GET_GITHUB,
    POST_LIKE,
    POST_COMMENT,
    POST_SHARE_POST
} from '../actions/types.js';
import _, { initial } from 'lodash';

const initialState = {
    post: {},
    inbox: {},
    githu: {},
    like: {},
    comment: {},
    share_post: {}
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
        case GET_GITHUB:
            return {
                ...state,
                github: action.payload
            }
        case POST_LIKE:
            return {
                ...state,
                like: action.payload
            }
        case POST_COMMENT:
            return {
                ...state,
                comment: action.payload
            }
        case POST_SHARE_POST:
            return {
                ...state,
                share_post: action.payload
            }
        default:
            return state;
    }
}