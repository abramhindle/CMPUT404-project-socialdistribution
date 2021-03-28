import React from "react";
import { message, Avatar, Button, Card, List, Popover, Tag, Tabs } from "antd";
import {
  UserOutlined,
  UserAddOutlined,
  HeartTwoTone,
  ShareAltOutlined,
  CommentOutlined,
  EditOutlined,
  DeleteOutlined,
} from "@ant-design/icons";
import CommentArea from "../CommentArea";
import { getCommentList } from "../../requests/requestComment";
import { postRequest } from "../../requests/requestFriendRequest";
import { getAuthorByAuthorID } from "../../requests/requestAuthor";
import EditPostArea from "../EditPostArea";
import ConfirmModal from "../ConfirmModal";
import CommentItem from "./CommentItem";
import { getLikes, sendLikes } from "../../requests/requestLike";
import { deletePost, sendPost } from "../../requests/requestPost";

const { TabPane } = Tabs;

const tagsColor = {
  Movies: "lime",
  Books: "blue",
  Music: "volcano",
  Sports: "cyan",
  Life: "gold",
};
export default class PostDisplay extends React.Component {
  state = {
    comments: [],
    isModalVisible: false,
    isEditModalVisible: false,
    isDeleteModalVisible: false,
    authorID: this.props.authorID,
    isLiked: false,
    isCommentLiked: false,
    likesList: [],
    commentLikeList: [],
    isShared:
      this.props.rawPost.source !== this.props.rawPost.origin ? true : false,
  };

  componentDidMount() {
    getCommentList({ postID: this.props.postID }).then((res) => {
      if (res.status === 200) {
        this.getCommentDataSet(res.data).then((value) => {
          this.setState({ comments: value });
        });
      }
    });
    getLikes({ _object: this.props.postID }).then((res) => {
      if (res.status === 200) {
        this.getLikeDataSet(res.data).then((val) => {
          this.setState({ likesList: val });
          this.state.likesList.forEach((item) => {
            if (item.authorID === this.state.authorID) {
              this.setState({ isLiked: true });
            }
          });
        });
      } else {
        message.error("Request failed!");
      }
    });
  }
  getCommentDataSet = (commentData) => {
    let promise = new Promise(async (resolve, reject) => {
      const commentsArray = [];
      for (const comment of commentData) {
        const authorInfo = await getAuthorByAuthorID({
          authorID: comment.author_id,
        });
        commentsArray.push({
          authorName: authorInfo.data.displayName,
          authorID: comment.author_id,
          comment: comment.comment,
          published: comment.published,
          commentid: comment.id,
          eachCommentLike: false,
          postID: comment.post_id,
          actor: this.state.authorID,
        });
      }
      resolve(commentsArray);
    });
    return promise;
  };
  getLikeDataSet = (likeData) => {
    let promise = new Promise(async (resolve, reject) => {
      const likeArray = [];

      for (const like of likeData) {
        const authorInfo = await getAuthorByAuthorID({
          authorID: like.author_id,
        });
        likeArray.push({
          authorName: authorInfo.data.displayName,
          authorID: like.author_id,
        });
      }
      resolve(likeArray);
    });
    return promise;
  };

  handleClickFollow = async () => {
    var n = this.props.postID.indexOf("/posts/");
    let params = {
      actor: this.props.authorID,
      object: this.props.postID.substring(0, n),
      summary: "I want to follow you!",
    };
    postRequest(params).then((response) => {
      if (response.status === 200) {
        message.success("Request sent!");
        window.location.reload();
      } else if (response.status === 409) {
        message.error("Invalid request!");
      } else {
        message.error("Request failed!");
      }
    });
  };

  handleClickReply = () => {
    this.setState({ isModalVisible: !this.state.isModalVisible });
  };

  handleClickShare = async () => {
    let params = this.props.rawPost;
    params.authorID = this.state.authorID;
    params.visibility = "FRIENDS";
    params.source = this.state.authorID;
    if (params.source !== params.origin) {
      sendPost(params).then((response) => {
        if (response.status === 200) {
          message.success("Post shared!");
          window.location.reload();
        } else {
          message.error("Whoops, an error occurred while sharing.");
        }
      });
    } else {
      message.error("You cannot share your own post.");
    }
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

  handleClickLike = () => {
    if (this.state.isLiked === false) {
      this.setState({
        isLiked: true,
      });

      let params = {
        postID: this.props.postID,
        actor: this.props.authorID,
        object: this.props.postID,
        summary: "I like your post!",
        context: this.props.postID,
      };

      sendLikes(params).then((response) => {
        if (response.status === 200) {
          message.success("Likes sent!");
        } else {
          message.error("Likes failed!");
        }
      });
    } else {
      this.setState.isLiked = true;
    }
  };
  commentLikes = () => {
    this.setState({ isModalVisible: !this.state.isModalVisible });
  };

  clickLikeComment = (item) => {
    if (item.eachCommentLike === false) {
      this.setState({
        eachCommentLike: true,
      });

      let params = {
        postID: this.props.postID,
        actor: this.props.authorID,
        object: item.commentid,
        summary: "I like your comment!",
        context: this.props.postID,
      };
      sendLikes(params).then((response) => {
        if (response.status === 200) {
          message.success("Likes sent!");
        } else {
          message.error("Likes failed!");
        }
      });
    }
  };

  render() {
    const {
      title,
      authorName,
      github,
      content,
      datetime,
      postID,
      categories,
      enableEdit,
    } = this.props;

    const userInfo = (
      <div>
        <p>{authorName}</p>
        <p>{github}</p>
        <Button icon={<UserAddOutlined />} onClick={this.handleClickFollow} />
      </div>
    );

    const editButton = enableEdit ? (
      <Button
        type="text"
        style={{ color: "#C5C5C5" }}
        onClick={this.handleClickEdit}
      >
        <EditOutlined /> Edit
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
        <DeleteOutlined /> Delete
      </Button>
    ) : (
      ""
    );

    const likeIconColor = this.state.isLiked ? "#eb2f96" : "#A5A5A5";

    const tags =
      categories !== undefined
        ? categories.map((tag) => (
            <Tag key={tag} color={tagsColor[tag]}>
              {tag}
            </Tag>
          ))
        : "";

    return (
      <div>
        <Card
          title={
            <span>
              <ShareAltOutlined
                style={{
                  color: "#4E89FF",
                  display: this.state.isShared ? "" : "none",
                }}
              />
              {"  " + title}
            </span>
          }
          extra={
            <span>
              <Popover content={userInfo} title="User Info" trigger="click">
                <Avatar icon={<UserOutlined />} /> {authorName}
              </Popover>
            </span>
          }
        >
          <div style={{ margin: "24px", textAlign: "center" }}>{content}</div>
          <div style={{ margin: "16px 0" }}>{tags}</div>
          <div>
            <HeartTwoTone
              twoToneColor={likeIconColor}
              onClick={this.handleClickLike}
            />
            <Button
              type="text"
              style={{ color: "#C5C5C5" }}
              onClick={this.handleClickReply}
            >
              <CommentOutlined /> Reply to
            </Button>

            <Button
              type="text"
              style={{ color: "#C5C5C5" }}
              onClick={this.handleClickShare}
            >
              <ShareAltOutlined /> Share
            </Button>
            {editButton}
            {deleteButton}
            <p
              style={{
                color: "#C5C5C5",
                fontSize: "small",
                float: "right",
              }}
            >
              {datetime}
            </p>
          </div>
          <div
            style={{
              clear: "both",
            }}
          />
          <Tabs
            defaultActiveKey="comments"
            type="card"
            size="small"
            style={{
              marginTop: "16px",
            }}
          >
            <TabPane tab="Comments" key="comments">
              {this.state.comments.length === 0 ? (
                ""
              ) : (
                <List
                  bordered
                  dataSource={this.state.comments}
                  renderItem={(item) => (
                    <List.Item>
                      <List.Item.Meta
                        avatar={<Avatar icon={<UserOutlined />} />}
                        title={item.authorName}
                        description={item.published}
                      />
                      {item.comment}
                      <CommentItem item={item} />
                    </List.Item>
                  )}
                />
              )}
            </TabPane>
            <TabPane tab="Likes" key="likes">
              {this.state.likesList.length === 0 ? (
                ""
              ) : (
                <List
                  dataSource={this.state.likesList}
                  renderItem={(item) => (
                    <List.Item>
                      <List.Item.Meta
                        avatar={<Avatar icon={<UserOutlined />} />}
                        title={item.authorName}
                        description={"likes this post."}
                      />
                    </List.Item>
                  )}
                />
              )}
            </TabPane>
          </Tabs>

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
            handleConfirmModalVisiblility={
              this.handleDeletePostModalVisiblility
            }
            dosomething={this.deleteSelectedPost}
          />
        </Card>
      </div>
    );
  }
}
