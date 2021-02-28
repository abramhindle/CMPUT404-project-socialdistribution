import axios from 'axios';
import { POST_REGISTER } from './types';

// Register a new user
export const postRegister = (user) => dispatch => {
    axios.post('/api/auth/register', user)
        .then(res => {
            dispatch({
                type: POST_REGISTER,
                payload: res.data
            });
        }).catch(err => console.log(err));
}
