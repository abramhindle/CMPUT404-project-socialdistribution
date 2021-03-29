import axios from 'axios';
import { POST_REGISTER, POST_LOGIN, POST_SEARCH_DISPLAYNAME, POST_FRIEND_REQUEST, GET_GITHUB, POST_UPDATE_PROFILE } from './types';
import { returnErrors } from './messages';

// Register a new user
export const postRegister = (user) => dispatch => {
    axios.post('/api/auth/register', user)
        .then(res => {
            dispatch({
                type: POST_REGISTER,
                payload: res.data
            });
        }).catch(err => dispatch(returnErrors(err.response.data, err.response.status)));
}

export const postLogin = (user) => dispatch => {
    axios.post('/api/auth/login', user)
        .then(res => {
            dispatch({
                type: POST_LOGIN,
                payload: res.data
            });
        }).catch(err => dispatch(returnErrors(err.response.data, err.response.status)));
}

export const postSearchDisplayName = (displayName) => dispatch => {
    axios.post('api/query/displayName', displayName)
        .then(res => {
            dispatch({
                type: POST_SEARCH_DISPLAYNAME,
                payload: res.data
            });
        }).catch(err => dispatch(returnErrors(err.response.data, err.response.status)));
}

export const postFriendRequest = (request, object_id) => dispatch => {
    axios.post(`author/${object_id}/inbox`, request)
        .then(res => {
            dispatch({
                type: POST_FRIEND_REQUEST,
                payload: res.data
            });
        }).catch(err => dispatch(returnErrors(err.response.data, err.response.status)));
}

export const getGithub = (github) => dispatch => {
    axios.get(`https://api.github.com/users/${github}/events/public`)
        .then(res => {
            dispatch({
                type: GET_GITHUB,
                payload: res.data
            });
        }).catch(err => dispatch(returnErrors(err.response.data, err.response.status)));
}

export const postUpdateProfile = (user) => dispatch => {
    axios.post(user.id, user)
        .then(res => {
            dispatch({
                type: POST_UPDATE_PROFILE,
                payload: res.data
            });
        }).catch(err => dispatch(returnErrors(err.response.data, err.response.status)));
}