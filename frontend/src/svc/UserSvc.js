import axios from 'axios';

/*
 * This file will contains all logic pertaining to API consumption
 */
export const UserSvc = {
    Login:  ({username, password}) => {
        // Perform validation on username and password here if needed
        console.log('Login values of form: ', username, password);
        return axios.post('/author/login', {username, password}); 
    },

    Register: ({username, github_url, password}) => {
        console.log('Register values of form: ', username, password, github_url);
        return axios.post('/author/register', {username, password, github_url});
    }
}

