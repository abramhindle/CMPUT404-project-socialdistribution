import React from "react";
import { List, message, Avatar } from "antd";
import { UserOutlined } from "@ant-design/icons";
import { getFriendList } from "../../requests/requestFriends";
import { 
  getFollowerList,
  getFollower,
} from "../../requests/requestFollower";
import {
  getAuthorByAuthorID,
  getRemoteAuthorByAuthorID,
} from "../../requests/requestAuthor";
import SingleFriend from "../SingleFriend";
import { getFriendDataSet } from "../Utils";
import { getHostname } from "../Utils";
import { auth } from "../../requests/URL";

export default class Friends extends React.Component {
  constructor(props) {
    super(props);
    this._isMounted = false;
    this.state = {
      authorID: this.props.authorID,
      friends: [],
      remoteFriendList: [],
    };
  }

  componentDidMount() {
    this._isMounted = true;
    let remoteFriends = [];
    let localFriends = [];
    getFollowerList({ object: this.state.authorID }).then((res) => {
      console.log("resData", res.data);
      if (res.data.items.length !== 0) {
        console.log("you have followers", res.data.items.length);
        for (const follower_id of res.data.items) {
          let host = getHostname(follower_id);
          let n = this.state.authorID.indexOf("/author/");
          let length = this.state.authorID.length;
          let params = {
              actor: this.state.authorID.substring(n + 8, length),
              object: follower_id,
            }
          if (host !== window.location.hostname) {
            params.remote = true;
            params.auth = auth;
            getFollower(params).then((response) => {
              console.log("response:", response);
              if (response.data.exist) {
                console.log("I found a remote friend", follower_id);
                getRemoteAuthorByAuthorID({
                  URL: follower_id,
                  auth: auth,
                }).then((response2) => {
                  const obj = {
                    displayName: response2.data.displayName,
                    github: response2.data.github,
                    id: response2.data.id,
                  };
                  remoteFriends.push(obj);
                  this.setState({ 
                    friends: localFriends,
                    remoteFriendList: remoteFriends,
                  });
                });
                
                
              } else {
                console.log("Not a remote friend", follower_id);
              } 
            });
          } else {
            params.auth = auth;
            params.remote = false;
            getFollower(params).then((response) => {
              console.log("response2:", response);
              if (response.data.exist) {
                console.log("I found a local friend", follower_id);
                getAuthorByAuthorID({
                  authorID: follower_id,
                }).then((response2) => {
                  const obj = {
                    displayName: response2.data.displayName,
                    github: response2.data.github,
                    id: response2.data.id,
                  };
                  localFriends.push(obj);
                  this.setState({ 
                    friends: localFriends,
                    remoteFriendList: remoteFriends,
                  });
                });
                
                
              } else {
                console.log("Not a local friend", follower_id);
              } 
            });
          }
        }
      }
    });
  }

  componentWillUnmount() {
    this._isMounted = false;
  }

  render() {
    const allFriends = this.state.friends.concat(this.state.remoteFriendList);
    return (
      <div style={{ margin: "0 20%" }}>
        <List
          bordered
          dataSource={allFriends}
          renderItem={(item) => (
            <List.Item>
              <List.Item.Meta
                avatar={<Avatar icon={<UserOutlined />} />}
                title={item.displayName}
                description={item.github}
              />
              <SingleFriend
                authorID={this.state.authorID}
                friendID={item.id}
              />
            </List.Item>
          )}
        />
      </div>
    );
  }
}
