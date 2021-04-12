import axios from 'axios';
import {
    POST_REGISTER,
    POST_LOGIN,
    POST_SEARCH_DISPLAYNAME,
    POST_FRIEND_REQUEST,
    GET_GITHUB,
    POST_UPDATE_PROFILE,
    GET_FRIENDS,
    GET_FOLLOWERS,
    UPDATE_AUTH,
    GET_ERRORS,
    GET_SUCCESS,
    GET_PERSONAL_POSTS,
    DELETE_FRIEND,
    GET_FOLLOWING
} from './types';
import { returnErrors } from './messages';

// Register a new user
export const postRegister = (user) => dispatch => {
    axios.post('/api/auth/register', user)
        .then(res => {
            dispatch({
                type: POST_REGISTER,
                payload: res.data
            });
        }).catch(err => {
            const errors = {
                msg: err.response.data,
                origin: POST_REGISTER,
                status: err.response.status
            }
            dispatch({
                type: GET_ERRORS,
                payload: errors
            })
        });
}

export const postLogin = (user) => dispatch => {
    axios.post('/api/auth/login', user)
        .then(res => {
            dispatch({
                type: POST_LOGIN,
                payload: res.data
            });
        }).catch(err => {
            const errors = {
                msg: err.response.data,
                origin: POST_LOGIN,
                status: err.response.status
            }
            dispatch({
                type: GET_ERRORS,
                payload: errors
            })
        });
}

export const updateAuth = (username, password) => dispatch => {
    dispatch({
        type: UPDATE_AUTH,
        payload: btoa(`${username}:${password}`)
    });
}

export const postSearchDisplayName = (token) => dispatch => {
    axios.get('/authors?more=True', {
            headers: {
                'Authorization': `Basic ${token}`
            }
        }).then(res => {
            dispatch({
                type: POST_SEARCH_DISPLAYNAME,
                payload: res.data
            });
        }).catch(err => {
            const errors = {
                msg: err.response.data,
                origin: POST_SEARCH_DISPLAYNAME,
                status: err.response.status
            }
            dispatch({
                type: GET_ERRORS,
                payload: errors
            })
        });
}

export const postFriendRequest = (request, author, recipient, token) => dispatch => {
    axios.put(`/followers/${recipient}/followers/${author}`, request, {
            headers: {
                'Authorization': `Basic ${token}`
            }
        }).then(res => {
            dispatch({
                type: POST_FRIEND_REQUEST,
                payload: res.data
            });
            dispatch({
                type: GET_SUCCESS,
                payload: {
                    status: 200,
                    origin: POST_FRIEND_REQUEST
                }
            });
        }).catch(err => {
            const errors = {
                msg: err.response.data,
                origin: POST_FRIEND_REQUEST,
                status: err.response.status
            }
            dispatch({
                type: GET_ERRORS,
                payload: errors
            })
        });
}

export const getGithub = (github) => dispatch => {
    axios.get(`https://api.github.com/users/${github}/events/public`)
        .then(res => {
            dispatch({
                type: GET_GITHUB,
                payload: res.data
            });
        }).catch(err => {
            const errors = {
                msg: err.response.data,
                origin: GET_GITHUB,
                status: err.response.status
            }
            dispatch({
                type: GET_ERRORS,
                payload: errors
            })
        });
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
    }).catch(err => {
        const errors = {
            msg: err.response.data,
            origin: POST_UPDATE_PROFILE,
            status: err.response.status
        }
        dispatch({
            type: GET_ERRORS,
            payload: errors
        })
    });
}

export const getFriends = (author_id, token) => dispatch => {
    axios.get(`author/${author_id}/friends`, {
            headers: {
                'Authorization': `Basic ${token}`
            }
        }).then(
            res => {
                dispatch({
                    type: GET_FRIENDS,
                    payload: res.data
                });
        }).catch(err => {
            const errors = {
                msg: err.response.data,
                origin: GET_FRIENDS,
                status: err.response.status
            }
            dispatch({
                type: GET_ERRORS,
                payload: errors
            })
        });
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
        }).catch(err => {
            const errors = {
                msg: err.response.data,
                origin: GET_FOLLOWERS,
                status: err.response.status
            }
            dispatch({
                type: GET_ERRORS,
                payload: errors
            })
        });
}

export const getFollowing = (author_id, token) => dispatch => {
    axios.get(`author/${author_id}/following`, {
            headers: {
                'Authorization': `Basic ${token}`
            }
        }).then(res => {
            dispatch({
                type: GET_FOLLOWING,
                payload: res.data
            });
        }).catch(err => {
            const errors = {
                msg: err.response.data,
                origin: GET_FOLLOWING,
                status: err.response.status
            }
            dispatch({
                type: GET_ERRORS,
                payload: errors
            })
        });
}


export const deleteFriend = (author, friend, token) => dispatch => {
    axios.delete(`${author.url}/followers/${_.last(friend.url.split('/'))}`, {
            headers: {
                'Authorization': `Basic ${token}`
            }
        }).then(res => {
            dispatch({
                type: GET_SUCCESS,
                payload: {
                    status: 200,
                    origin: DELETE_FRIEND
                }
            });
        }).catch(err => {
            const errors = {
                msg: err.response.data,
                origin: DELETE_FRIEND,
                status: err.response.status
            }
            dispatch({
                type: GET_ERRORS,
                payload: errors
            })
        });
}

