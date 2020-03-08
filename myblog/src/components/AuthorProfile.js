import React, { Component } from 'react'
import 'antd/dist/antd.css';
import { Button } from 'antd';
import './AuthorProfile.css'
import axios from 'axios';

class AuthorProfile extends React.Component {
    state = {
        userName: "User",
    };

    componentDidMount() {
        axios.get('http://localhost:8000/api/user/author/current_user/', { headers: { 'Authorization': 'Token ' + document.cookie } })
          .then(res => {
            this.setState({UserName: res.data.username})
            console.log(this.state.userName);
        //     const MyPost = res.data;
        //     this.setState({MyPostData: MyPost});
        //     if(MyPost.displayName === ''){
        //         this.setState({displayedName: MyPost.userName})
        //     }
        //     else{
        //         this.setState({displayedName: MyPost.displayName})
        //     }
        //     console.log(this.state.displayedName)    
        //   })
         
        //   .catch(function (error) {
        //   console.log(error);
          });
      };
    


    render() {
        return (
            <div className="profile">     
                {/* {this.state.persons.map(person => {person.username})} */}
                {/* <span>User Name: {this.state.person}</span> */}
                {/* <span>Email: user1@gmail.com </span> */}
                <Button>Edit</Button>
                <hr/>
            </div>
        )
    }
}

export default AuthorProfile
