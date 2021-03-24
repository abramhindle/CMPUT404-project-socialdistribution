import React from "react";
import { Modal, Card, Tag, Button, message, Image, Avatar } from "antd";
import { UserOutlined, UserSwitchOutlined } from "@ant-design/icons";
import { deleteFollower } from "../../requests/requestFollower";
import UnfollowModal from "../UnfollowModal";


export default class SingleFriend extends React.Component {
  constructor(props) {
    super(props);
    this._isMounted = false;
    this.state = {
      isModalVisible: false,
      friendName: this.props.friendName,
      friendID: this.props.friendID,
      github: this.props.github,
      ButtonDisabled: false,
      authorID : this.props.authorID,
    };
  }


  handleClickUnfollow = () => {
    this.setState({ isModalVisible: !this.state.isModalVisible });
  };

  handleModalVisibility = () => {
    this.setState({ isModalVisible: !this.state.isModalVisible });
  };

  removeFollower = () => {
    var n = this.props.authorID.indexOf("/author/")
    var length = this.props.authorID.length;
    let params = {
      actor: this.props.authorID.substring(n+8,length),
      object: this.props.friendID,

    };
    deleteFollower(params).then((response) => {
      if (response.status === 200) {
        message.success("Successfully unfollowed.");
        window.location.reload();
        //window.location.reload();
      } else {
        message.error("Unfollow Failed!");
      }
    });
  }

  render() {
    const { authorID, friendID, friendName, github } = this.state;
    const friendHeader = (
      <div>
        <Avatar icon={<UserOutlined />} /> 
        <Button
          style={{float: 'right'}}
          icon={<UserSwitchOutlined />}
          onClick={this.handleClickUnfollow}
        ></Button>
        <p>{friendName}</p>
      </div>
    );
    return (
      <Card size="small" title={friendHeader} style={{ width: 600 }}>
        <UnfollowModal
          visible={this.state.isModalVisible}
          handleModalVisibility={this.handleModalVisibility}
          dosomething={this.removeFollower}
        />
      </Card>
    );
  }
}
