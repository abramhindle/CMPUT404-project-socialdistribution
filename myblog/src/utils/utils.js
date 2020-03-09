import cookie from 'react-cookies';
import axios from 'axios' ;

function validateCookie () {
    if(cookie.load('token')){
        const token = cookie.load('token');
        const headers = {
            'Authorization': 'Token '.concat(token)
          }
          axios.get('http://localhost:8000/api/user/author/current_user/',{headers : headers})
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

export default validateCookie;