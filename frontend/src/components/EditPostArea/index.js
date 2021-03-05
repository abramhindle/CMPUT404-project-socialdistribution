import React from "react";
import { message, Modal } from "antd";
import { updatePost } from "../../requests/requestPost";
import Post from "../Post";

export default class EditPostArea extends React.Component {
  state = {
    postObj: {},
  };

  handleModalOk = () => {
    //post comment
    if (this.state.postObj !== {}) {
      updatePost(this.state.postObj).then((res) => {
        if (res.status === 200) {
          message.success("Comment post success!");
          window.location.reload();
        } else {
          message.error("Comment send fails");
        }
      });
      this.props.handleEditPostModalVisiblility();
    }
  };

  handleModalCancel = () => {
    this.props.handleEditPostModalVisiblility();
  };

  handlePostEdit = (newPostObj) => {
    this.setState({ postObj: newPostObj });
  };

  render() {
    return (
      <Modal
        title="Comment"
        visible={this.props.visible}
        onOk={this.handleModalOk}
        onCancel={this.handleModalCancel}
      >
        <Post
          authorID={this.props.authorID}
          postID={this.props.postID}
          enableEdit={true}
        />
      </Modal>
    );
  }
}
