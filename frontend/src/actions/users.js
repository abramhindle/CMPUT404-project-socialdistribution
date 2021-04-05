import axios from 'axios';
import { POST_REGISTER, POST_LOGIN, POST_SEARCH_DISPLAYNAME, POST_FRIEND_REQUEST, GET_GITHUB, POST_UPDATE_PROFILE, GET_FRIENDS, GET_FOLLOWERS, UPDATE_AUTH, GET_REMOTE_AUTHORS, GET_KONNECT_REMOTE_AUTHORS } from './types';
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

export const updateAuth = (username, password) => dispatch => {
    dispatch({
        type: UPDATE_AUTH,
        payload: btoa(`${username}:${password}`)
    });
}

export const postSearchDisplayName = (displayName, token) => dispatch => {
    axios.post('api/query/displayName', displayName, {
            headers: {
                'Authorization': `Basic ${token}`
            }
        }).then(res => {
            dispatch({
                type: POST_SEARCH_DISPLAYNAME,
                payload: res.data
            });
        }).catch(err => dispatch(returnErrors(err.response.data, err.response.status)));
}

export const postSearchDisplayNameRemote = (displayName, token) => dispatch => {
    axios.post('https://konnect-testing.herokuapp.com/api/query/displayName', displayName, {
            headers: {
                'Authorization': `Basic ${token}`,
            }
        }).then(res => {
            dispatch({
                type: GET_KONNECT_REMOTE_AUTHORS,
                payload: res.data
            });
        }).catch(err => dispatch(returnErrors(err.response.data, err.response.status)));
}


export const postFriendRequest = (request, url, token) => dispatch => {
    axios.post(`${url}/inbox`, request, {
            headers: {
                'Authorization': `Basic ${token}`
            }
        }).then(res => {
                dispatch({
                    type: POST_FRIEND_REQUEST,
                    payload: res.data
                });
            }).catch(err => dispatch(returnErrors(err.response.data, err.response.status)));
}

export const postFriendRequestRemote = (request, url, token) => dispatch => {
    axios.post(`${url}/inbox`, request, {
            headers: {
                'Authorization': `Basic ${btoa('konnectnode:thisiskonnect')}`
            }
        }).then(res => {
                dispatch({
                    type: POST_FRIEND_REQUEST,
                    payload: res.data
                });
            }).catch(err => dispatch(returnErrors(err.response.data, err.response.status)));
}


export const postRemoteFriendRequest = (request, object, author_id, token) => dispatch => {
    axios.put(`${object.host}api/author/${object.id}/followers/${author_id}/`, request, {
            headers: {
                'Authorization': `Basic ${token}`,
                'Access-Control-Allow-Origin': '*'
            }
        }).then(res => {
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

export const postUpdateProfile = (user, token) => dispatch => {
    axios.post(user.url + "/", user, {
        headers: {
            'Authorization': `Basic ${token}`
        }
    }).then(res => {
            dispatch({
                type: POST_UPDATE_PROFILE,
                payload: res.data
            });
        }).catch(err => dispatch(returnErrors(err.response.data, err.response.status)));
}

export const getFriends = (author_id, token) => dispatch => {
    axios.get(`author/${author_id}/friends`, {
            headers: {
                'Authorization': `Basic ${token}`
            }
        }).then(res => {
            dispatch({
                type: GET_FRIENDS,
                payload: res.data
            });
        }).catch(err => dispatch(returnErrors(err.response.data, err.response.status)));
}

export const getFollowers = (author_id, token) => dispatch => {
    axios.get(`author/${author_id}/followers`, {
            headers: {
                'Authorization': `Basic ${token}`
            }
        }).then(res => {
            dispatch({
                type: GET_FOLLOWERS,
                payload: res.data
            });
        }).catch(err => dispatch(returnErrors(err.response.data, err.response.status)));
}

// test003
// 
export const getRemoteAuthors = (token) => dispatch => {
    axios.get(`https://konnection-server.herokuapp.com/api/authors/`, {
            headers: {
                'Authorization': `Basic ${token}`
            }
        }).then(res => {
                dispatch({
                    type: GET_REMOTE_AUTHORS,
                    payload: res.data
                });
            }).catch(err => dispatch(returnErrors(err.response.data, err.response.status)));
}
