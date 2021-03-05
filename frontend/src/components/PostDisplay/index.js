import React from "react";
import { Avatar, Button, Card, List, Divider, message } from "antd";
import { UserOutlined, LikeOutlined, DislikeOutlined } from "@ant-design/icons";
import CommentArea from "../CommentArea";
import { getCommentList } from "../../requests/requestComment";
import EditPostArea from "../EditPostArea";
import ConfirmModal from "../ConfirmModal";
import { deletePost } from "../../requests/requestPost";

export default class PostDisplay extends React.Component {
  constructor(props) {
    super(props);
    this._isMounted = false;
    this.state = {
      comments: [],
      isModalVisible: false,
      isEditModalVisible: false,
      isDeleteModalVisible: false,
      authorID: this.props.authorID,
    };
  }

  componentDidMount() {
    getCommentList({ postID: this.props.postID }).then((res) => {
      if (res.status === 200) {
        this.setState({ comments: res.data });
      }
    });
  }

  handleClickReply = () => {
    this.setState({ isModalVisible: !this.state.isModalVisible });
  };

  handleClickEdit = () => {
    this.setState({ isEditModalVisible: !this.state.isEditModalVisible });
  };

  handleClickDelete = () => {
    this.setState({ isDeleteModalVisible: !this.state.isDeleteModalVisible });
  };

  handleCommentModalVisiblility = () => {
    this.setState({ isModalVisible: !this.state.isModalVisible });
  };

  handleEditPostModalVisiblility = () => {
    this.setState({ isEditModalVisible: !this.state.isEditModalVisible });
  };

  handleDeletePostModalVisiblility = () => {
    this.setState({ isDeleteModalVisible: !this.state.isDeleteModalVisible });
  };

  deleteSelectedPost = () => {
    deletePost({ postID: this.props.postID }).then((res) => {
      if (res.status === 200) {
        window.location.reload();
      } else {
        message.error("Fail to delete the post.");
      }
    });
  };

  handleClickDislike = () => {
    //TODO
  };

  handleClickLike = () => {
    //TPDP
  };

  render() {
    const {
      title,
      authorName,
      content,
      datetime,
      postID,
      enableEdit,
    } = this.props;
    console.log("post display", this.props.authorID);

    const editButton = enableEdit ? (
      <Button
        type="text"
        style={{ color: "#C5C5C5" }}
        onClick={this.handleClickEdit}
      >
        Edit
      </Button>
    ) : (
      ""
    );

    const deleteButton = enableEdit ? (
      <Button
        type="text"
        style={{ color: "#C5C5C5" }}
        onClick={this.handleClickDelete}
      >
        Delete
      </Button>
    ) : (
      ""
    );

    return (
      <div>
        <Card
          title={title}
          extra={
            <span>
              <Avatar icon={<UserOutlined />} />
              <p>{authorName}</p>
            </span>
          }
        >
          <div style={{ margin: "24px", textAlign: "center" }}>{content}</div>
          <p>{datetime}</p>
          <div>
            <Button icon={<LikeOutlined />} onClick={this.handleClickLike} />
            <Button
              icon={<DislikeOutlined onClick={this.handleClickDislike} />}
            />
            <Button
              type="text"
              style={{ color: "#C5C5C5" }}
              onClick={this.handleClickReply}
            >
              Reply to
            </Button>
            {editButton}
            {deleteButton}
          </div>
          <Divider orientation="left">Comments</Divider>
          <List
            bordered
            pagination={true}
            dataSource={this.state.comments}
            renderItem={(item) => (
              <List.Item>
                <Avatar icon={<UserOutlined />} />
                <p>{item.comment}</p>
              </List.Item>
            )}
          />
          <CommentArea
            authorID={this.props.authorID}
            postID={postID}
            visible={this.state.isModalVisible}
            handleCommentModalVisiblility={this.handleCommentModalVisiblility}
          />
          <EditPostArea
            authorID={this.props.authorID}
            postID={postID}
            visible={this.state.isEditModalVisible}
            handleEditPostModalVisiblility={this.handleEditPostModalVisiblility}
          />
          <ConfirmModal
            visible={this.state.isDeleteModalVisible}
            handleEditPostModalVisiblility={this.handleEditPostModalVisiblility}
            dosomething={this.deleteSelectedPost}
          />
        </Card>
      </div>
    );
  }
}
