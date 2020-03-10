import cookie from 'react-cookies';
import axios from 'axios' ;

const host_name = "localhost:8000";
const protocol = "http://"
const token_url = protocol+host_name+'/api/user/author/current_user/'

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
export default validateCookie;