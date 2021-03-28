import axios from 'axios';
import { GET_POST, POST_NEWPOST, GET_INBOX, POST_LIKE } from './types';
import { returnErrors } from './messages';

// get a post using an authorId and postId (more should be added, such as server id etc.)
export const getPost = (authorId, postId) => dispatch => {
    axios.get(`/author/${authorId}/posts/${postId}`)
        .then(res => {
            dispatch({
                type: GET_POST,
                payload: res.data
            });
        }).catch(err => dispatch(returnErrors(err.response.data, err.response.status)));
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
        }).catch(err => dispatch(returnErrors(err.response.data, err.response.status)));
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
        }).catch(err => dispatch(returnErrors(err.response.data, err.response.status)));
}

export const getGithub = (github_id) => dispatch => {
    axios.get(`https://api.github.com/users/${github_id}/events/public`)
        .then(res => {
            dispatch({
                type: GET_INBOX,
                payload:res.data
            });
        }).catch(err => dispatch(returnErrors(err.response.data, err.response.status)));
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
        }).catch(err => dispatch(returnErrors(err.response.data, err.response.status)));
}
