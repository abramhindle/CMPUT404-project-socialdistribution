import React from "react";
import { List, message, Avatar, Button, Input, Modal, Card } from "antd";
import { UserOutlined } from "@ant-design/icons";
import moment from "moment";
/*import { postComment } from "../../requests/requestComment";*/

const { TextArea } = Input;

export default class CommentArea extends React.Component {
  state = {
    comments: [],
    submitting: false,
    commentValue: "",
  };

  handleCommentSubmit = () => {
    if (!this.state.commentValue) {
      return;
    }

    this.setState({
      submitting: true,
    });

    setTimeout(() => {
      this.setState({
        submitting: false,
        commentValue: "",
        comments: [
          ...this.state.comments,
          {
            author: "Han Solo",
            avatar:
              "https://zos.alipayobjects.com/rmsportal/ODTLcjxAfvqbxHnVXCYX.png",
            content: <p>{this.state.commentValue}</p>,
            datetime: moment().fromNow(),
          },
        ],
      });
    }, 1000);
  };

  handleCommentChange = (e) => {
    this.setState({
      commentValue: e.target.value,
    });
  };
/*
  handleModalOk = () => {
    //post comment
    let params = {
      comment: this.state.commentValue,
      contentType: "text/markdown",
    };
    postComment(params).then((res) => {
      if (res.status === 200) {
        message.success("Comment post success!");
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
*/
  render() {
    const { title, authorName } = this.props;
    return (
      <Modal
        title="Comment"
        visible={this.props.visible}
        onOk={this.handleModalOk}
        onCancel={this.handleModalCancel}
      >
        <div>
          <TextArea
            onChange={this.onContentChange}
            placeholder="Write comment..."
            autoSize={{ minRows: 3, maxRows: 5 }}
            allowClear
            style={{ margin: "24px 24px" }}
          />
        </div>
      </Modal>
    );
  }
}
