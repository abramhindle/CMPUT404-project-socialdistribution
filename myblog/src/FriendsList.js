import React from 'react';
import 'antd/dist/antd.css';
import './index.css';
import { List, Avatar, Button, Skeleton, Modal } from 'antd';

import reqwest from 'reqwest';

const { confirm } = Modal;

const count = 6;
const fakeDataUrl = `https://randomuser.me/api/?results=${count}&inc=name,gender,email,nat&noinfo`;

function showDeleteConfirm() {
  confirm({
    title: 'Are you sure you want to unfriend this friend?',
    okText: 'Yes',
    okType: 'danger',
    cancelText: 'No',
    onOk() {
      console.log('OK');
    },
    onCancel() {
      console.log('Cancel');
    },
  });
}

class FriendsList extends React.Component {
  state = {
    initLoading: true,
    loading: false,
    data: [],
    list: [],
  };

  componentDidMount() {
    this.getData(res => {
      this.setState({
        initLoading: false,
        data: res.results,
        list: res.results,
      });
    });
  }

  getData = callback => {
    reqwest({
      url: fakeDataUrl,
      type: 'json',
      method: 'get',
      contentType: 'application/json',
      success: res => {
        callback(res);
      },
    });
  };

  onLoadMore = () => {
    this.setState({
      loading: true,
      list: this.state.data.concat([...new Array(count)].map(() => ({ loading: true, name: {} }))),
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

    const { initLoading, loading, list } = this.state;

    const loadMore =
      !initLoading && !loading ? (
        <div style={loadmorestyle}>
          <Button onClick={this.onLoadMore}>loading more</Button>
        </div>
      ) : null;

    return (
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
                title={<a href="https://ant.design">{item.name.last}</a>}
              />
            </Skeleton>
            <div style={unfriendstyle} onClick={showDeleteConfirm}>
              <Button size={size} >Unfriend</Button>
            </div>
          </List.Item>
        )}
      />
    );
  }
}

export default FriendsList;
