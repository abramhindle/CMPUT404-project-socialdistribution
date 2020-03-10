import React from 'react';
import 'antd/dist/antd.css';
import './index.css';
import { List, Avatar, Button, Skeleton, Modal } from 'antd';
import './components/Header.css';
import AuthorHeader from './components/AuthorHeader';
import axios from 'axios';
import cookie from 'react-cookies';
import validateCookie from './utils/utils.js';

const { confirm } = Modal;

const URL = `http://localhost:8000/api/friend/my_friends/`;

class FriendsList extends React.Component {
  state = {
    initLoading: true,
    loading: false,
    data: [],
    list: [],
    current_user : "",
    isloading : true
  };

  componentDidMount() {
    validateCookie();
    this.fetchData();
  }

  fetchData = () => {
    this.getData(res => {
      this.setState({
        initLoading: false,
        data: res.data,
        list: res.data,
        size: res.data.length
      });
    });
    this.getUser();
  }

  getUser = () => {
    const token = cookie.load('token');
    const headers = {
      'Authorization': 'Token '.concat(token)
    }
    axios.get("http://localhost:8000/api/user/author/current_user/",{headers : headers})
    .then(res => {
      this.setState({
        current_user:res.data['username'],
        isloading:false
       })
    } )
    .catch(function (error) {
      console.log(error)
    });
  }

  showDeleteConfirm(friend_request_id, f1Id) {
    const that = this;
    const token = cookie.load('token');
    const headers = {
      'Authorization': 'Token '.concat(token)
    }
    const data = {
      "f1Id" : f1Id,
      "status" : "R"
    }
    confirm({
      title: 'Are you sure you want to unfriend this friend?',
      okText: 'Yes',
      okType: 'danger',
      cancelText: 'No',
      onOk() {
        axios.patch("http://localhost:8000/api/friend/my_friends/".concat(friend_request_id).concat('/'), data, {headers : headers})
        .then(res => {
          that.fetchData();
        }).catch(function (error) {
          console.log(error)
        });
      },
      onCancel() {
        console.log('Cancel');
      },
    });
  }

  getData = callback => {

    const token = cookie.load('token');
    const headers = {
      'Authorization': 'Token '.concat(token)
    }
    axios.get(URL,{headers : headers})
    .then(res => {
      callback(res)
    } )
    .catch(function (error) {
      console.log(error)
    });
  };

  render() {
    const liststyle = {
        backgroundColor: "white",
        padding: "1%",
    }  

    const unfriendstyle={
      height: "3%",
      width: "10%",
      right: "1%",
    }

    const titlestyle={
      fontSize : 18 
    }

    const { initLoading, list, current_user } = this.state;

    return (!this.state.isloading ? 
        <div>
        <AuthorHeader/>
        <List
            className="demo-loadmore-list"
            loading={initLoading}
            itemLayout="horizontal"
            dataSource={list}
            style={liststyle}
            renderItem={item => (
            <List.Item>
                <Skeleton avatar title={false} loading={item.loading} active>
                <List.Item.Meta
                    avatar={
                      <Avatar
                      style={{
                        color: '#f56a00',
                        backgroundColor: '#fde3cf',
                      }}
                    >
                      {item.f1Id !== current_user ? item.f1Id[0].toUpperCase() : item.f2Id[0].toUpperCase()}
                    </Avatar>
                    }
                    title={<a style={titlestyle} href={"/author/profile?username=".concat(item.f1Id !== current_user ? item.f1Id : item.f2Id)}>{item.f1Id !== current_user ? item.f1Id : item.f2Id}</a>}
                />
                </Skeleton>
                <div style={unfriendstyle} onClick={() => this.showDeleteConfirm(item.id,item.f1Id !== current_user ? item.f1Id : item.f2Id)}>
                <Button type="danger" shape="round" size={'medium'} >Unfriend</Button>
                </div>
            </List.Item>
            )}
        />
      </div> : null
    );
  }
}

export default FriendsList;
