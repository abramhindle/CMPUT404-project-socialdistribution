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
            isSelf: this.props.isSelf,
            isFriend: false,
            isPending: false,
        };

    }

    componentWillMount() {
        validateCookie();
    }

    componentDidMount() {
        const token = cookie.load('token');
        const headers = {
          'Authorization': 'Token '.concat(token)
        }
        axios.get('http://localhost:8000/api/user/author/'.concat(this.props.username).concat("/"), 
        { headers: headers}).then(res => {
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

        if (!this.props.isSelf) {
            axios.get('http://localhost:8000/api/friend/if_friend/'.concat(this.props.username).concat("/"), 
            { headers: headers}).then(res => {
                var status = res.data.status;
                if (status === "friend") {
                    this.setState({
                        isFriend: true,
                    })
                } else if (status === "pending") {
                    this.setState({
                        isPending: true,
                    })
                }
            }).catch((error) => {
                  console.log(error);
            });
        }
    };

    sendFriendRequest(username) {
        const token = cookie.load('token');
        const headers = {
          'Authorization': 'Token '.concat(token)
        }
        axios.post("http://localhost:8000/api/friend/friend_request/",
        {
            f2Id: username,
        },{headers: headers}
        ).then(res => {
            this.setState({
                isPending: true,
            })
        })
        .catch(function (error) {
          console.log(error);
        });
    }

    render() {
        const {username, isSelf, isFriend, isPending} = this.state;
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
                {isFriend || isPending ? null : <button onClick={() => this.sendFriendRequest(username)}><Icon type="user-add"/><span>Add Friend</span></button>}
                {isPending ? <span className="pending-box">Pending...</span> : null}
                <hr/>
            </div>
        );
    }
}

export default AuthorProfile
