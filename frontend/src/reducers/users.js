// evaluate action and send down certain state depending on action
import { POST_LOGIN, POST_REGISTER, POST_SEARCH_DISPLAYNAME, POST_FRIEND_REQUEST, GET_GITHUB, GET_FRIENDS, GET_FOLLOWERS } from '../actions/types.js';

const initialState = {
    user: {},
    displayNameSearchResult: [],
    friendRequest: {},
    github_activity: [],
    friends: {items:[]},
    followers: {items:[]},
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
        default:
            return state;
    }
}