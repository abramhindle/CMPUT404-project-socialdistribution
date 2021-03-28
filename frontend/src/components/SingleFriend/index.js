import React from "react";
import { Button, message } from "antd";
import { UserSwitchOutlined } from "@ant-design/icons";
import { deleteFollower } from "../../requests/requestFollower";
import UnfollowModal from "../UnfollowModal";

export default class SingleFriend extends React.Component {
  constructor(props) {
    super(props);
    this._isMounted = false;
    this.state = {
      isModalVisible: false,
      friendID: this.props.friendID,
      github: this.props.github,
      ButtonDisabled: false,
      authorID: this.props.authorID,
    };
  }

  handleClickUnfollow = () => {
    this.setState({ isModalVisible: !this.state.isModalVisible });
  };

  handleModalVisibility = () => {
    this.setState({ isModalVisible: !this.state.isModalVisible });
  };

  removeFollower = () => {
    var n = this.props.authorID.indexOf("/author/");
    var length = this.props.authorID.length;
    let params = {
      actor: this.props.authorID.substring(n + 8, length),
      object: this.props.friendID,
    };
    deleteFollower(params).then((response) => {
      if (response.status === 200) {
        message.success("Successfully unfollowed.");
        window.location.reload();
      } else {
        message.error("Unfollow Failed!");
      }
    });
  };

  render() {
    return (
      <div>
        <Button style={{ float: "right" }} onClick={this.handleClickUnfollow}>
          {<UserSwitchOutlined />} Unfollow
        </Button>
        <UnfollowModal
          visible={this.state.isModalVisible}
          handleModalVisibility={this.handleModalVisibility}
          dosomething={this.removeFollower}
        />
      </div>
    );
  }
}
