import axios from 'axios';
import { GET_POST, POST_NEWPOST } from './types';
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
export const postNewPost = (post) => dispatch => {
    axios.post(`/author/${post.author_id}/posts/`, post)
        .then(res => {
            dispatch({
                type: POST_NEWPOST,
                payload: res.data
            });
        }).catch(err => dispatch(returnErrors(err.response.data, err.response.status)));
}