import React from "react";
import { List, message, Avatar } from "antd";
import { UserOutlined } from "@ant-design/icons";
import { getFriendList } from "../../requests/requestFriends";
import SingleFriend from "../SingleFriend";
import { getFriendDataSet } from "../Utils";

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
        getFriendDataSet(res.data).then((value) => {
          this.setState({ friends: value });
        });
      } else {
        message.error("No friends detected...");
      }
    });
  }

  render() {

    return (
      <div style={{ margin: "0 20%" }}>
        <List
          bordered
          dataSource={this.state.friends}
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
