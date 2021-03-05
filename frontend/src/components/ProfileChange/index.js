import React from "react";
import { message, Input, Modal } from "antd";
import { updateAuthor } from "../../requests/requestAuthor";

const{ TextArea } = Input;

export default class ProfileChange extends React.Component {

  state = {
    authorID: this.props.authorID,
    displayName: this.props.displayName,
    github: this.props.github,
    newName: this.props.displayName,
    newGithub: this.props.github,
  };


  handleModalOk = () => {
    let params = {
      authorID: this.state.authorID,
      displayName: this.state.newName,
      github: this.state.newGithub,
    }
    updateAuthor(params).then((res) => {
      if (res.status === 204) {
        message.success("Update Info successfully!");
      } else {
        message.error("Info update fails");
      }
    });
    this.props.handleChangeModalVisibility();
  };

  handleModalCancel = () => {
    this.props.handleChangeModalVisibility();
  };

  onNameChange = ({ target: { value } }) => {
    this.setState({ newName: value });
  };

  onGithubChange = ({ target: { value } }) => {
    this.setState({ newGithub: value });
  };


  render() {
    console.log("post22", this.state.github);
    return (
      <Modal
        title="Update Info"
        visible={this.props.visible}
        onOk={this.handleModalOk}
        onCancel={this.handleModalCancel}
      >
        <TextArea
          onChange={this.onNameChange}
          placeholder={this.state.displayName}
          autoSize={{ minRows: 1, maxRows: 3 }}
          allowClear
          style={{ margin: "24px 24px" }}
        />
        <TextArea
          onChange={this.onGithubChange}
          placeholder={this.state.github}
          autoSize={{ minRows: 1, maxRows: 3 }}
          allowClear
          style={{ margin: "24px 24px" }}
        />
      </Modal>
    );
  }
}

