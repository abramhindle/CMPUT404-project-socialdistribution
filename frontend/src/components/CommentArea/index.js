import React from "react";
import { message, Input, Modal } from "antd";
import { postComment } from "../../requests/requestComment";

const { TextArea } = Input;

export default class CommentArea extends React.Component {
  state = {
    commentValue: "",
  };

  handleCommentChange = (e) => {
    this.setState({
      commentValue: e.target.value,
    });
  };

  handleModalOk = () => {
    //post comment
    let params = {
      author: this.props.authorID,
      postID: this.props.postID,
      comment: this.state.commentValue,
      contentType: "text/markdown",
    };
    postComment(params).then((res) => {
      if (res.status === 200) {
        message.success("Comment post success!");
        window.location.reload();
      } else {
        message.error("Comment send fails");
      }
    });
    this.props.handleCommentModalVisiblility();
  };

  handleModalCancel = () => {
    this.props.handleCommentModalVisiblility();
  };

  onContentChange = ({ target: { value } }) => {
    this.setState({ commentValue: value });
  };

  render() {
    return (
      <Modal
        title="Comment"
        visible={this.props.visible}
        onOk={this.handleModalOk}
        onCancel={this.handleModalCancel}
      >
        <TextArea
          onChange={this.onContentChange}
          placeholder="Write comment..."
          autoSize={{ minRows: 3, maxRows: 5 }}
          allowClear
          style={{ margin: "24px 24px" }}
        />
      </Modal>
    );
  }
}
