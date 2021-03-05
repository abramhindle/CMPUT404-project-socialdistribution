import React, { useState } from "react";
import { Button, Descriptions, Modal, Form, Input, Radio } from "antd";
import { getAuthorUseID } from "../../requests/requestAuthor";
import ProfileChange from "../ProfileChange"

export default class Profile extends React.Component {
  constructor(props) {
    super(props);
    this._isMounted = false;

    this.state = {
      authorID: this.props.authorID,
      username: this.props.username,
      displayName: this.props.displayName,
      github: this.props.github,
      isModalVisible: false,
    };
  }

  componentDidMount() {
    this._isMounted = true;
    
    getAuthorUseID({authorID: this.props.authorID}).then((res) => {
      this.state.displayName = res.data.displayName;
      this.state.github = res.data.github;
    });
    if (this.state.authorID === "" && this._isMounted) {
      this.setState({ authorID: this.props.authorID });
      
    }
  }

  handleClick = () => {
    this.setState({ isModalVisible: !this.state.isModalVisible });
  };

  handleChangeModalVisibility = () => {
    this.setState({ isModalVisible: !this.state.isModalVisible });
  };

  render() {
    console.log("post22", this.state.github);
    return (
      <div style={{ margin: "10% 10%" }}>
        <Descriptions title="User Info">
          <Descriptions.Item label="UserName">{this.state.username}</Descriptions.Item>
          <Descriptions.Item label="displayName">{this.state.displayName}</Descriptions.Item>
          <Descriptions.Item label="github">{this.state.github}</Descriptions.Item>
        </Descriptions>
        {/* change info */}
        <Button type="primary" onClick={this.handleClick}>
          Change Info
        </Button>
        {/* logout */}
        <Button type="primary" danger onClick={this.props.logout}>
          Logout
        </Button>
      <ProfileChange
        authorID={this.props.authorID}
        displayName={this.state.displayName}
        github={this.state.github}
        visible={this.state.isModalVisible}
        handleChangeModalVisibility={this.handleChangeModalVisibility}
      />
      </div>
    );
  }
}

