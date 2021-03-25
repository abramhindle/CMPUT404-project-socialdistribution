import React from "react";
import { message, Input, Modal } from "antd";
import { updateAuthor } from "../../requests/requestAuthor";

const { TextArea } = Input;

export default class ProfileChange extends React.Component {
  state = {
    authorID: this.props.authorID,
    newName: this.props.displayName,
    newGithub: this.props.github,
    displayNameValue: "",
    githubValue: "",
  };

  handleModalOk = () => {
    let params = {
      authorID: this.state.authorID,
      displayName: this.state.newName,
      github: this.state.newGithub,
    };
    updateAuthor(params).then((res) => {
      if (res.status === 204) {
        message.success("Update Info successfully!");
      } else {
        message.error("Info update fails");
      }
    });
    this.props.handleChangeModalVisibility();
    this.setState({ displayNameValue: "", githubValue: "" });
  };

  handleModalCancel = () => {
    this.props.handleChangeModalVisibility();
    this.setState({ displayNameValue: "", githubValue: "" });
  };

  onNameChange = ({ target: { value } }) => {
    this.setState({ newName: value, displayNameValue: value });
  };

  onGithubChange = ({ target: { value } }) => {
    this.setState({ newGithub: value, githubValue: value });
  };

  render() {
    return (
      <Modal
        title="Update Info"
        visible={this.props.visible}
        onOk={this.handleModalOk}
        onCancel={this.handleModalCancel}
      >
        <TextArea
          value={this.state.newName}
          onChange={this.onNameChange}
          autoSize
          allowClear
        />
        <TextArea
          value={this.state.newGithub}
          onChange={this.onGithubChange}
          autoSize
          allowClear
        />
      </Modal>
    );
  }
}
