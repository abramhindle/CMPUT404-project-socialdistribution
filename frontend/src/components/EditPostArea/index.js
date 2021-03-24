import React from "react";
import { Modal } from "antd";
import Post from "../Post";

export default class EditPostArea extends React.Component {
  handleModalCancel = () => {
    this.props.handleEditPostModalVisiblility();
  };

  render() {
    return (
      <Modal
        title="Edit"
        visible={this.props.visible}
        onCancel={this.handleModalCancel}
        okButtonProps={{ style: { display: "none" } }}
      >
        <Post
          authorID={this.props.authorID}
          postID={this.props.postID}
          enableEdit={true}
          handleModalOk={this.handleModalOk}
        />
      </Modal>
    );
  }
}
