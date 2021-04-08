import axios from 'axios';
import {
    GET_POST,
    POST_NEWPOST,
    GET_INBOX,
    POST_LIKE,
    POST_COMMENT,
    GET_LIKES,
    GET_SUCCESS,
    GET_ERRORS,
    POST_SHARE_POST
} from './types';
import { returnErrors } from './messages';

// get a post using an authorId and postId (more should be added, such as server id etc.)
export const getPost = (authorId, postId) => dispatch => {
    axios.get(`/author/${authorId}/posts/${postId}`)
        .then(res => {
            dispatch({
                type: GET_POST,
                payload: res.data
            });
        }).catch(err => {
            const errors = {
                msg: err.response.data,
                origin: GET_POST,
                status: err.response.status
            }
            dispatch({
                type: GET_ERRORS,
                payload: errors
            })
        });
}

// Create a new Post
export const postNewPost = (post, token) => dispatch => {
    axios.post(`/author/${post.author_id}/posts/`, post, {
        headers: {
            'Authorization': `Basic ${token}`
        }
    }).then(res => {
        dispatch({
            type: POST_NEWPOST,
            payload: res.data
        });
        dispatch({
            type: GET_SUCCESS,
            payload: {
                status: 200,
                origin: POST_NEWPOST
            }
        });
    }).catch(err => {
        const errors = {
            msg: err.response.data,
            origin: POST_NEWPOST,
            status: err.response.status
        }
        dispatch({
            type: GET_ERRORS,
            payload: errors
        })
    });
}

// Get all posts for activity feed
export const getInbox = (authorId, token) => dispatch => {
    axios.get(`/author/${authorId}/inbox`, {
        headers: {
            'Authorization': `Basic ${token}`
        }
    }).then(res => {
        dispatch({
            type: GET_INBOX,
            payload: res.data
        });
    }).catch(err => {
        const errors = {
            msg: err.response.data,
            origin: GET_INBOX,
            status: err.response.status
        }
        dispatch({
            type: GET_ERRORS,
            payload: errors
        })
    });
}

export const postLike = (body, post_author_id, token) => dispatch => {
    axios.post(`/author/${post_author_id}/inbox`, body, {
        headers: {
            'Authorization': `Basic ${token}`
        }
    }).then(res => {
        dispatch({
            type: POST_LIKE,
            payload: res.data
        });
        dispatch({
            type: GET_SUCCESS,
            payload: {
                status: 200,
                origin: POST_LIKE
            }
        });
    }).catch(err => {
        const errors = {
            msg: err.response.data,
            origin: POST_LIKE,
            status: err.response.status
        }
        dispatch({
            type: GET_ERRORS,
            payload: errors
        })
    });
}

export const postComment = (body, url, token) => dispatch => {
    axios.post(url + '/comments', body, {
        headers: {
            'Authorization': `Basic ${token}`
        }
    }).then(res => {
        dispatch({
            type: POST_COMMENT,
            payload: res.data
        });
        dispatch({
            type: GET_SUCCESS,
            payload: {
                status: 200,
                origin: POST_COMMENT
            }
        });
    }).catch(err => {
        const errors = {
            msg: err.response.data,
            origin: POST_COMMENT,
            status: err.response.status
        }
        dispatch({
            type: GET_ERRORS,
            payload: errors
        })
    });
}

export const getLikes = (url, token) => dispatch => {
    axios.get(url, {
        headers: {
            'Authorization': `Basic ${token}`
        }
    }).then(res => {
        dispatch({
            type: GET_LIKES,
            payload: res.data
        });
    }).catch(err => {
        const errors = {
            msg: err.response.data,
            origin: GET_LIKES,
            status: err.response.status
        }
        dispatch({
            type: GET_ERRORS,
            payload: errors
        })
    });
}

export const postSharePost = (post, token, destination) => dispatch => {
    axios.post(`${destination.id}/inbox`, post, {
        headers: {
            'Authorization': `Basic ${token}`
        }
    }).then(res => {
        dispatch({
            type: POST_SHARE_POST,
            payload: res.data
        });
        dispatch({
            type: GET_SUCCESS,
            payload: {
                status: 200,
                origin: POST_SHARE_POST
            }
        });
    }).catch(err => {
        const errors = {
            msg: err.response.data,
            origin: POST_SHARE_POST,
            status: err.response.status
        }
        dispatch({
            type: GET_ERRORS,
            payload: errors
        })
    });
}