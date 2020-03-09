import React, { Component } from 'react'
import 'antd/dist/antd.css';
import { Icon, Button } from 'antd';
import './AuthorProfile.css'
import axios from 'axios';
import cookie from 'react-cookies';

class AuthorProfile extends React.Component {
    constructor(props) {
        super(props)
    
        this.state = {
            userName: null,
            email: null,
            displayName: null,
            github: null,
            bio: null,
            // isEdit: false,
        }

        // this.clickHandler = this.clickHandler.bind(this)
    }

    componentDidMount() {
        axios.get('http://localhost:8000/api/user/author/current_user/', 
        { headers: { 'Authorization': 'Token ' + cookie.load('token')}}).then(res => {
            var userInfo = res.data;
            this.setState({userName: userInfo.username});
            this.setState({email: userInfo.email});
            this.setState({displayName: userInfo.displayName});
            this.setState({github: userInfo.github});
            this.setState({bio: userInfo.bio});
          });
      };

    // clickHandler() {
    //     this.setState({
    //         isEdit: true
    //     })
    // }

    render() {
        return (           
            <div className="user">
                <span className="tag">User Name: <span className="info">{this.state.userName}</span></span>
                <span className="secondtag">Email: <span className="info">{this.state.email}</span></span>
                <br/>
                <span className="tag">Display Name: <span className="info">{this.state.displayName}</span></span>
                <span className="secondtag">Github: <span className="info">{this.state.github}</span></span>
                <br/>
                <span className="tag">Bio: <span className="info">{this.state.bio}</span></span>
                <a href="/Settings">
                    <Icon type="edit" />
                </a>
                {/* <Button icon="edit" href="http://www.google.com"></Button>   */}
                <hr/>
            </div>
        );
    }
}

export default AuthorProfile
