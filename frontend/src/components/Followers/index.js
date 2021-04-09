import React from "react";
import { List, Avatar } from "antd";
import { UserOutlined } from "@ant-design/icons";
import { getFollowerList } from "../../requests/requestFollower";
import {
  getAuthorByAuthorID,
  getRemoteAuthorByAuthorID,
} from "../../requests/requestAuthor";
import { getDomainName } from "../Utils";
import { domainAuthPair } from "../../requests/URL";

export default class Followers extends React.Component {
  constructor(props) {
    super(props);
    this._isMounted = false;
    this.state = {
      authorID: this.props.authorID,
      followers: [],
    };
  }

  componentDidMount() {
    this._isMounted = true;
    let followerList = [];
    getFollowerList({ object: this.state.authorID }).then((res) => {
      if (res.data.items.length !== 0) {
        for (const follower_id of res.data.items) {
          let domain = getDomainName(follower_id);
          if (domain !== window.location.hostname) {
            getRemoteAuthorByAuthorID({
              URL: follower_id,
              auth: domainAuthPair[domain],
            }).then((response2) => {
              const obj = {
                displayName: response2.data.displayName,
                github: response2.data.github,
                id: response2.data.id,
              };
              followerList.push(obj);
              this.setState({
                followers: followerList,
              });
            });
          } else {
            getAuthorByAuthorID({
              authorID: follower_id,
            }).then((response2) => {
              const obj = {
                displayName: response2.data.displayName,
                github: response2.data.github,
                id: response2.data.id,
              };
              followerList.push(obj);
              this.setState({
                followers: followerList,
              });
            });
          }
        }
      } else {
        console.log("No followers...");
      }
    });
  }

  componentWillUnmount() {
    this._isMounted = false;
  }

  render() {
    return (
      <div style={{ margin: "0 20%" }}>
        <List
          bordered
          dataSource={this.state.followers}
          renderItem={(item) => (
            <List.Item>
              <List.Item.Meta
                avatar={<Avatar icon={<UserOutlined />} />}
                title={item.displayName}
                description={item.github}
              />
            </List.Item>
          )}
        />
      </div>
    );
  }
}
