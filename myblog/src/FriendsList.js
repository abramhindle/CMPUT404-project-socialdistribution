import React from 'react';
import 'antd/dist/antd.css';
import './index.css';
import { List, Avatar, Button, Skeleton, Modal } from 'antd';
import './components/Header.css';
import AuthorHeader from './components/AuthorHeader';
import axios from 'axios';
import cookie from 'react-cookies';

const { confirm } = Modal;

const URL = `http://localhost:8000/api/friend/my_friends/`;

class FriendsList extends React.Component {
  state = {
    initLoading: true,
    loading: false,
    data: [],
    list: [],
    current_user : "",
  };

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
    axios.get("http://localhost:8000/api/user/author/current_user/",{headers : headers})
    .then(res => {
      this.setState({current_user:res.data['username']})
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
      console.log(res.data);
      callback(res)
    } )
    .catch(function (error) {
      console.log(error)
    });
  };

  onLoadMore = () => {
    this.setState({
      loading: true,
      list: this.state.data.concat([...new Array(this.state.size)].map(() => ({ loading: true, name: {} }))),
    });
    this.getData(res => {
      const data = this.state.data.concat(res.results);
      this.setState(
        {
          data,
          list: data,
          loading: false,
        },
        () => {     
          window.dispatchEvent(new Event('resize'));
        },
      );
    });
  };

  render() {
    const liststyle = {
        backgroundColor: "white",
        padding: "1%",
    }  
    
    const loadmorestyle={
      textAlign: 'center',
      marginTop: 12,
      height: 32,
      lineHeight: '4%',
      backgroundColor: "white",
    }

    const unfriendstyle={
      height: "3%",
      width: "10%",
      right: "1%",
    }

    const { size } = this.state;
    const { initLoading, loading, list, current_user } = this.state;

    const loadMore =
      !initLoading && !loading ? (
        <div style={loadmorestyle}>
          <Button onClick={this.onLoadMore}>loading more</Button>
        </div>
      ) : null;

    return (
        <div>
        <AuthorHeader/>
        <List
            className="demo-loadmore-list"
            loading={initLoading}
            itemLayout="horizontal"
            loadMore={loadMore}
            dataSource={list}
            style={liststyle}
            renderItem={item => (
            <List.Item>
                <Skeleton avatar title={false} loading={item.loading} active>
                <List.Item.Meta
                    avatar={
                    <Avatar src="https://zos.alipayobjects.com/rmsportal/ODTLcjxAfvqbxHnVXCYX.png" />
                    }
                    title={<a href={"http://localhost:8000/api/user/author/".concat(current_user)}>{item.f1Id !== current_user ? item.f1Id : item.f2Id}</a>}
                />
                </Skeleton>
                <div style={unfriendstyle} onClick={() => this.showDeleteConfirm(item.id,item.f1Id !== current_user ? item.f1Id : item.f2Id)}>
                <Button size={size} >Unfriend</Button>
                </div>
            </List.Item>
            )}
        />
      </div>
    );
  }
}

export default FriendsList;
