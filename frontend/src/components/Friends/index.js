import React from "react";
import { Button, Modal, List, Avatar } from "antd";
import { UserOutlined, UserSwitchOutlined } from "@ant-design/icons";

export default class Friends extends React.Component {
  constructor(props) {
    super(props);
    this._isMounted = false;
    this.state = {
      authorID: this.props.authorID,
      friends: [],
    };
  }

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
              <p>{item.comment}</p>
              <Button icon={<UserSwitchOutlined />}></Button>
            </List.Item>
          )}
        />
      </div>
    );
  }
}
