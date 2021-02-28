import axios from 'axios';
import { POST_REGISTER } from './types';

// Register a new user
export const postRegister = () => dispatch => {
    axios.get('/api/auth/register')
        .then(res => {
            dispatch({
                type: POST_REGISTER,
                payload: res.data
            });
        }).catch(err => console.log(err));
}
