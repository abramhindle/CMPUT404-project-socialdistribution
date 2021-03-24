import React from "react";
import { Button, List, Avatar, message } from "antd";
import { getFriendList } from "../../requests/requestFriends";
import SingleFriend from "../SingleFriend";

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


  render() {
    return (
      <div style={{ margin: "10% 20%" }}>
        <List
          bordered
          pagination={true}
          dataSource={this.state.friends}
          renderItem={(item) => (
            <List.Item>
              <SingleFriend
                authorID={this.state.authorID}
                friendID={item.id}
                friendName={item.displayName}
                friendGithub={item.github}
              />
            </List.Item>
          )}  
        />
      </div>
    );
  }
}
