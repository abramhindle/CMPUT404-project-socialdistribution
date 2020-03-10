import React, {Component} from 'react';
import 'antd/dist/antd.css';
import { Icon } from 'antd';
import './AuthorProfile.css'
import axios from 'axios';
import cookie from 'react-cookies';
import validateCookie from '../utils/utils.js';

class AuthorProfile extends Component {

    constructor(props) {
        super(props)
    
        this.state = {
            username: this.props.username,
            isSelf: this.props.isSelf
        };
    }

    componentWillMount() {
        validateCookie();
    }

    componentDidMount() {
        axios.get('http://localhost:8000/api/user/author/'.concat(this.props.username).concat("/"), 
        { headers: { 'Authorization': 'Token ' + cookie.load('token')}}).then(res => {
            var userInfo = res.data;
            this.setState({
                email: userInfo.email,
                displayName: userInfo.displayName,
                github: userInfo.github,
                bio: userInfo.bio
            });
          }).catch((error) => {
              console.log(error);
          });
    };

    render() {
        const {isSelf} = this.state;
        return (           
            <div className="user">
                <span className="tag">User Name: <span className="info">{this.state.username}</span></span>
                <span className="secondtag">Email: <span className="info">{this.state.email}</span></span>
                <br/>
                <span className="tag">Display Name: <span className="info">{this.state.displayName}</span></span>
                <span className="secondtag">Github: <span className="info">{this.state.github}</span></span>
                <br/>
                <span className="tag">Bio: <span className="info">{this.state.bio}</span></span>
                {isSelf ? <a href="/settings"><Icon type="edit" /></a> : null}
                <hr/>
            </div>
        );
    }
}

export default AuthorProfile
