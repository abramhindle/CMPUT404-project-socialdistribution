import React from "react";
import { Button, List, Avatar, message } from "antd";
import { UserOutlined, UserSwitchOutlined } from "@ant-design/icons";
import { getFriendList } from "../../requests/requestFriends";
// import { domain, port } from "../../requests/URL";

export default class Friends extends React.Component {
  constructor(props) {
    super(props);
    this._isMounted = false;
    this.state = {
      authorID: this.props.authorID,
      friends: [],
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
  }

  clickFollowBtn = () => {};

  render() {
    return (
      <div style={{ margin: "10% 20%" }}>
        <List
          bordered
          pagination={true}
          dataSource={this.state.friends}
          renderItem={(item) => (
            <List.Item>
              <Avatar icon={<UserOutlined />} />
              <p>{item.displayName}</p>
              <Button
                icon={<UserSwitchOutlined />}
                onClick={this.clickFollowBtn}
              ></Button>
            </List.Item>
          )}
        />
      </div>
    );
  }
}
