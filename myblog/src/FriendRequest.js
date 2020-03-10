import React from 'react';
import 'antd/dist/antd.css';
import './index.css';
import { List, Avatar, Button, Skeleton, Modal } from 'antd';
import './components/Header.css'
import AuthorHeader from './components/AuthorHeader'
import cookie from 'react-cookies';
import axios from 'axios';
import validateCookie from './utils/utils.js';
import {FRIEND_REQUEST_API,FETCH_POST_API} from "./utils/constants.js";
const { confirm } = Modal;



class FriendRequest extends React.Component {
  state = {
    initLoading: true,
    loading: false,
    data: [],
    list: [],
    current_user : "",
    isloading : true
  };

  componentWillMount() {
    validateCookie();
  }

  componentDidMount() {
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
    axios.get(FETCH_POST_API,{headers : headers})
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

  showConfirm(decision,status,f1Id,friend_request_id) {
    const that = this;
    const token = cookie.load('token');
    const headers = {
      'Authorization': 'Token '.concat(token)
    }
    const data = {
      "f1Id" : f1Id,
      "status" : status
    }
    confirm({
      title: 'Are you sure you want to ' + decision + ' this friend request?',
      okText: 'Yes',
      okType: 'danger',
      cancelText: 'No',
      onOk() {
        axios.patch(FRIEND_REQUEST_API.concat(friend_request_id).concat('/'), data, {headers : headers})
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
    axios.get(FRIEND_REQUEST_API,{headers : headers})
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

    const buttonstyle={
        marginRight: 30,
    }

    const titlestyle={
        fontSize : 18 
    }

    const { initLoading, list } = this.state;

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
                          {item.f1Id[0].toUpperCase()}
                        </Avatar>
                        }
                        title={<a style={titlestyle} href={"/author/profile?username=".concat(item.f1Id)}>{item.f1Id}</a>}
                    />
                    </Skeleton>
                    <Button type="primary" shape="round" size={'medium'} style={buttonstyle} onClick={() => this.showConfirm("accept","A",item.f1Id,item.id)}>Accept</Button>
                    <Button type="danger" shape="round"size={'medium'} style={buttonstyle} onClick={() => this.showConfirm("reject","R",item.f1Id,item.id)}>Reject</Button>
                </List.Item>
                )}
            />
        </div> : null
    );
  }
}

export default FriendRequest;
