import React from "react";
import { List, message, Avatar } from "antd";
import { UserOutlined } from "@ant-design/icons";
import { 
  getFriendList,
  getRemoteFriendList,
} from "../../requests/requestFriends";
import SingleFriend from "../SingleFriend";
import { auth } from "../../requests/URL";

export default class Friends extends React.Component {
  constructor(props) {
    super(props);
    this._isMounted = false;
    this.state = {
      authorID: this.props.authorID,
      friends: [],
      remoteFriends: [],
      remote: false,
    };
  }

  componentDidMount() {
    getFriendList({ authorID: this.state.authorID }).then((res) => {
      if (res.status === 200) {
        this.setState({ friends: res.data });
      } else {
        message.error("No friends detected...");
      }
    });
    getRemoteFriendList({
      // URL: `${remoteDomain4}/posts/`,
      // auth: auth4,
      URL: `${remoteDomain}/friends-list/`,
      auth: auth,
    }).then((res) => {
      if (res === 200) {
        this.setState({ remoteFriends: res.data });
      } else {
        message.error("No remote friends detected...");
      }
    });
  }

  render() {
    const allFriends = this.state.friends.concat(
      this.state.remoteFriends
    );

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
                remote={this.state.remote}
              />
            </List.Item>
          )}
        />
      </div>
    );
  }
}
