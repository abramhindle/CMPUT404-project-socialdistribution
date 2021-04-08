// evaluate action and send down certain state depending on action
import {
    POST_LOGIN,
    POST_REGISTER,
    POST_SEARCH_DISPLAYNAME,
    POST_FRIEND_REQUEST,
    GET_GITHUB,
    GET_FRIENDS,
    GET_FOLLOWERS,
    UPDATE_AUTH,
    GET_REMOTE_AUTHORS,
    GET_KONNECT_REMOTE_AUTHORS
} from '../actions/types.js';

const initialState = {
    user: {},
    user_id: '',
    displayNameSearchResult: [],
    friendRequest: {},
    github_activity: [],
    friends: {items:[]},
    followers: {items:[]},
    basic_token: '',
    remote_authors: [],
    konnect_remote_authors: []
}

export default function(state = initialState, action) {
    switch(action.type) {
        case POST_REGISTER:
            return {
                ...state,
                user: action.payload,
                user_id: action.payload.url.split('/')[4]
            };
        case POST_LOGIN:
            return {
                ...state,
                user: action.payload,
                user_id: action.payload.url.split('/')[4]
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
        case GET_FRIENDS:
            return {
                ...state,
                friends: action.payload
            }
        case GET_FOLLOWERS:
            return {
                ...state,
                followers: action.payload
            }
        case UPDATE_AUTH:
            return {
                ...state,
                basic_token: action.payload
            }
        case GET_REMOTE_AUTHORS:
            return {
                ...state,
                remote_authors: action.payload
            }
        case GET_KONNECT_REMOTE_AUTHORS:
            return {
                ...state,
                konnect_remote_authors: action.payload
            }
        default:
            return state;
    }
}