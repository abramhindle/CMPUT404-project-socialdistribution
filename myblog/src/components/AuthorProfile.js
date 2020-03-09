import React, {Component} from 'react';
import 'antd/dist/antd.css';
import { Icon } from 'antd';
import './AuthorProfile.css'
import axios from 'axios';
import cookie from 'react-cookies';

class AuthorProfile extends Component {

    constructor(props) {
        super(props)
    
        this.state = {
            username: this.props.username
        };
    }

    componentDidMount() {
        console.log(this.props.username)
        axios.get('http://localhost:8000/api/user/author/'.concat(this.props.username).concat("/"), 
        { headers: { 'Authorization': 'Token ' + cookie.load('token')}}).then(res => {
            var userInfo = res.data;
            this.setState({email: userInfo.email});
            this.setState({displayName: userInfo.displayName});
            this.setState({github: userInfo.github});
            this.setState({bio: userInfo.bio});
          }).catch((error) => {
              console.log(error);
          });
      };

    render() {
        return (           
            <div className="user">
                <span className="tag">User Name: <span className="info">{this.state.username}</span></span>
                <span className="secondtag">Email: <span className="info">{this.state.email}</span></span>
                <br/>
                <span className="tag">Display Name: <span className="info">{this.state.displayName}</span></span>
                <span className="secondtag">Github: <span className="info">{this.state.github}</span></span>
                <br/>
                <span className="tag">Bio: <span className="info">{this.state.bio}</span></span>
                <a href="/Settings"><Icon type="edit" /></a>
                <hr/>
            </div>
        );
    }
}

export default AuthorProfile
