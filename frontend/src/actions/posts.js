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
    POST_SHARE_POST,
    GET_PERSONAL_POSTS,
    DELETE_POST,
    PUT_UPDATE_POST,
    POST_PRIVATE_POST,
    POST_COMMENT_LIKE,
    GET_COMMENTS
} from './types';
import _ from 'lodash';
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
    axios.post(`/author/${_.last(post.author.url.split('/'))}/posts/`, post, {
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

export const postNewPrivatePost = (post, recipient, token) => dispatch => {
    axios.post(`/author/${_.last(post.author.url.split('/'))}/posts/?recipient=${recipient}`, post, {
        headers: {
            'Authorization': `Basic ${token}`
        }
    }).then(res => {
        dispatch({
            type: POST_PRIVATE_POST,
            payload: res.data
        });
        dispatch({
            type: GET_SUCCESS,
            payload: {
                status: 200,
                origin: POST_PRIVATE_POST
            }
        });
    }).catch(err => {
        const errors = {
            msg: err.response.data,
            origin: POST_PRIVATE_POST,
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

export const postLike = (body, author, token) => dispatch => {
    axios.post(`/author/${_.last(author.url.split('/'))}/inbox`, body, {
        headers: {
            'Authorization': `Basic ${token}`
        }
    }).then(res => {
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


export const postCommentLike = (body, author, token) => dispatch => {
    axios.post(`/author/${_.last(author.url.split('/'))}/inbox`, body, {
        headers: {
            'Authorization': `Basic ${token}`
        }
    }).then(res => {
        dispatch({
            type: GET_SUCCESS,
            payload: {
                status: 200,
                origin: POST_COMMENT_LIKE
            }
        });
    }).catch(err => {
        const errors = {
            msg: err.response.data,
            origin: POST_COMMENT_LIKE,
            status: err.response.status
        }
        dispatch({
            type: GET_ERRORS,
            payload: errors
        })
    });
}

export const postComment = (body, post, token) => dispatch => {
    axios.post(`/author/${_.last(post.author.id.split('/'))}/posts/${_.last(post.id.split('/'))}/comments`, body, {
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

export const getLikes = (item, token) => dispatch => {
    const items = item.id.split('/');
    axios.get(`/author/${items[items.length-3]}/post/${items[items.length-1]}/likes`, {
        headers: {
            'Authorization': `Basic ${token}`
        }
    }).then(res => {
        const payload = {
            itemData: res.data,
            itemId: item.id
        };
        dispatch({
            type: GET_LIKES,
            payload
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
    axios.put(`/author/${destination}/posts/${_.last(post.id.split('/'))}`, post, {
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

export const getPersonalPosts = (author, token) => dispatch => {
    axios.get(`/author/${_.last(author.url.split('/'))}/posts/`, {
            headers: {
                'Authorization': `Basic ${token}`
            }
        }).then(res => {
            dispatch({
                type: GET_PERSONAL_POSTS,
                payload: res.data
            });
        }).catch(err => {
            const errors = {
                msg: err.response.data,
                origin: GET_PERSONAL_POSTS,
                status: err.response.status
            }
            dispatch({
                type: GET_ERRORS,
                payload: errors
            })
        });
}

export const deletePost = (post, token) => dispatch => {
    const items = post.id.split('/');
    axios.delete(`/author/${items[items.length-3]}/posts/${items[items.length-1]}`, {
        headers: {
            'Authorization': `Basic ${token}`
        }
    }).then(res => {
        dispatch({
            type: GET_SUCCESS,
            payload: {
                status: 200,
                origin: DELETE_POST
            }
        });
    }).catch(err => {
        const errors = {
            msg: err.response.data,
            origin: DELETE_POST,
            status: err.response.status
        }
        dispatch({
            type: GET_ERRORS,
            payload: errors
        })
    });
}

export const putUpdatePost = (post, token) => dispatch => {
    const items = post.id.split('/');
    axios.post(`/author/${items[items.length-3]}/posts/${items[items.length-1]}`, post, {
        headers: {
            'Authorization': `Basic ${token}`
        }
    }).then(res => {
        dispatch({
            type: GET_SUCCESS,
            payload: {
                status: 200,
                origin: PUT_UPDATE_POST
            }
        });
    }).catch(err => {
        const errors = {
            msg: err.response.data,
            origin: PUT_UPDATE_POST,
            status: err.response.status
        }
        dispatch({
            type: GET_ERRORS,
            payload: errors
        })
    });
}

export const getComments = (item, token) => dispatch => {
    const items = item.id.split('/');
    axios.get(`/author/${items[items.length-3]}/posts/${items[items.length-1]}/comments`, {
        headers: {
            'Authorization': `Basic ${token}`
        }
    }).then(res => {
        const payload = {
            itemData: res.data,
            itemId: item.id
        };
        dispatch({
            type: GET_COMMENTS,
            payload
        });
    }).catch(err => {
        const errors = {
            msg: err.response.data,
            origin: GET_COMMENTS,
            status: err.response.status
        }
        dispatch({
            type: GET_ERRORS,
            payload: errors
        })
    });
}