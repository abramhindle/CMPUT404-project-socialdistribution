import axios from 'axios';
import { POST_NEWPOST } from './types';
import { returnErrors } from './messages';

// Register a new user
export const postNewPost = (post) => dispatch => {
    axios.post(`/author/${post.author_id}/posts/`, post)
        .then(res => {
            dispatch({
                type: POST_NEWPOST,
                payload: res.data
            });
        }).catch(err => dispatch(returnErrors(err.response.data, err.response.status)));
}