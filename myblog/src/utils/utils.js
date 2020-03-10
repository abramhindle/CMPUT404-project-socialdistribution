import cookie from 'react-cookies';
import axios from 'axios' ;
const token_url = 'http://localhost:8000/api/user/author/current_user/'

function validateCookie () {
    if(cookie.load('token')){
        const token = cookie.load('token');
        const headers = {
            'Authorization': 'Token '.concat(token)
          }
          axios.get(token_url,{headers : headers})
          .then(res => {
            return true;
          })
          .catch(function (error) {
            cookie.remove('token', { path: '/' });
            document.location.replace("/");
            return false;
          });
    }else{
        document.location.replace("/");
        return false;
    }
}

export const login_api = "http://127.0.0.1:8000/api/user/login/";
export const register_api="http://localhost:8000/api/user/signup/";
export const post_api = "http://localhost:8000/api/post/";
export const author_api = "http://localhost:8000/api/user/author/";
export const fetch_post_api = "http://localhost:8000/api/user/author/current_user/";
export const friend_api = "http://localhost:8000/api/friend/my_friends/";
export const friend_request_api="http://localhost:8000/api/friend/friend_request/"; 
export default validateCookie;