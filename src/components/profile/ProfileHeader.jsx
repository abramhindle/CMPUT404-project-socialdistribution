import React, { Component } from "react";
import "../../styles/profile/ProfileHeader.scss";
import EditOutlinedIcon from "@material-ui/icons/EditOutlined";
import Dropdown from "react-bootstrap/Dropdown";
import DropdownButton from "react-bootstrap/DropdownButton";
import EditProfileModal from "./EditProfileModal";

class ProfileHeader extends Component {
  constructor(props) {
    super(props);
    this.state = {
      username: "Username",
      remote: false,
      friend: true,
      following: true,
      isSelf: true,
      // isSelf will be changed by comparing the userID and the loggedIn user's id
      // to do: fetch the user
      modalShow: false,
    };
  }

  handleEditButtonClick = () => {
    // eslint-disable-next-line no-alert
    alert("todo");
  };

  renderModal = () => {
    const { modalShow } = this.state;
    if (modalShow) {
      this.setState({ modalShow: false });
    } else {
      this.setState({ modalShow: true });
    }
  };

  renderStatus = () => {
    const { isSelf, following, friend } = this.state;
    if (!isSelf) {
      if (!friend && !following) {
        return (this.renderFollowButton());
      }
      if (!friend && following) {
        return (this.renderDropDown(false));
      }
      return (this.renderDropDown(true));
    }
    return (this.renderEditProfileButton());
  };

  renderEditProfileButton = () => (
    <button
      type="button"
      className="edit-profile-button"
      onClick={this.renderModal}
    >
      <EditOutlinedIcon className="edit-icon" />
      <span>EDIT PROFILE</span>
    </button>
  );

  handleFollow = () => {
    this.setState({ following: true });
  };

  renderDropDown = (isFriend) => (
    <DropdownButton
      id="friend-status"
      title={isFriend === true ? "FRIENDS" : "FOLLOWING"}
      drop="down"
      alignRight
    >
      <Dropdown.Item onClick={this.handleUnFollow}>{isFriend === true ? "Unfriend" : "Unfollow"}</Dropdown.Item>
    </DropdownButton>
  );

  handleUnFollow = () => {
    this.setState({ friend: false, following: false });
  };

  renderFollowButton = () => (
    <button
      type="button"
      className="follow-button"
      onClick={this.handleFollow}
    >
      Follow
    </button>
  );

  render() {
    const { username, remote, modalShow } = this.state;
    return (
      <div className="profileHeader">
        <div className="image-section" />
        <div className="user-section">
          <div className="row1">
            <p>{username}</p>
            <p>{remote === true ? "Remote" : "Local"}</p>
          </div>
          <div className="row2">
            {this.renderStatus()}
            <EditProfileModal show={modalShow} onHide={this.renderModal} />
          </div>
        </div>
      </div>
    );
  }
}
export default ProfileHeader;
