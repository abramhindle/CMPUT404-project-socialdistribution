import React from "react";
import { message, Avatar, Button, Card, List, Popover, Tag, Tabs } from "antd";
import { UserOutlined, UserAddOutlined, HeartTwoTone } from "@ant-design/icons";
import CommentArea from "../CommentArea";
import { getCommentList } from "../../requests/requestComment";
import { postRequest } from "../../requests/requestFriendRequest";
import EditPostArea from "../EditPostArea";
import ConfirmModal from "../ConfirmModal";
import { deletePost,sendPost } from "../../requests/requestPost";

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
    likeslist: [],
  };

  componentDidMount() {
    getCommentList({ postID: this.props.postID }).then((res) => {
      if (res.status === 200) {
        this.setState({ comments: res.data });
      }
    });
  }

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
  // handleClickShare = () => {
  //   this.setState({ isModalVisible: !this.state.isModalVisible });
  // };
  handleClickShare = async () => {
    let params = this.props.rawPost;
    params.authorID = this.state.authorID;
    params.visibility = "FRIENDS";
    params.title = "Shared " + params.authorName + "\'s  \"" + params.title + "\"";
    console.log("hhh: " + JSON.stringify(params) );
    sendPost(params).then((response) => {
      if (response.status === 200) {
        message.success("Post shared!");
        // window.location.reload();
      } else {
        message.error("Cannot Share");
      }
    });
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
    if (this.state.isLiked === false) {
      this.setState(
        (prevState) => {
          console.log(prevState);
          return {
            isLiked: !prevState.isLiked,
            likeslist: [...this.state.likeslist, this.props.authorID],
          };
        },
        () => {
          console.log(this.state.likeslist);
        }
      );
      // var n = this.props.postID.indexOf("/likes/")
      // let params = {
      //   actor: this.props.authorID,
      //   object: this.props.postID.substring(0,n),
      //   summary: "I like you post!",
      //   context: "Post"
      // };
      // likesRequest(params).then((response) => {
      //   if (response.status === 200){
      //     message.success("Request sent!");
      //       window.location.reload();
      //     } else {
      //       message.error("Request failed!");
      //     }

      // });
    } else {
      this.setState(
        (prevState) => {
          return {
            isLiked: !prevState.isLiked,
            likeslist: this.state.likeslist.splice(
              this.state.likeslist.find(
                (item) => item.value === this.props.authorID
              ),
              1
            ),
          };
        },
        () => {
          console.log(this.state.likeslist);
        }
      );
    }
  };

  clickLikeComment = () => {};

  clickLikesButton = () => {};

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
          title={title}
          extra={
            <span>
              <Popover content={userInfo} title="User Info" trigger="click">
                <Avatar icon={<UserOutlined />} /> {authorName}
              </Popover>
            </span>
          }
        >
          <div style={{ margin: "24px", textAlign: "center" }}>{content}</div>
          <div style={{ margin: "24px" }}>{tags}</div>
          <div>
            <span onClick={() => this.handleClickLike()}>
              {this.state.isLiked ? "💓 Cancel" : "🖤 Like"}
            </span>
            <Button
              type="text"
              style={{ color: "#C5C5C5" }}
              onClick={this.clickLikesButton}
            >
              Likes
            </Button>
            <Button
              type="text"
              style={{ color: "#C5C5C5" }}
              onClick={this.handleClickReply}
            >
              Reply to
            </Button>
            <Button
              type="text"
              style={{ color: "#C5C5C5" }}
              onClick={this.handleClickShare}
            >
              Share
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
                        title={authorName}
                        description={item.published}
                      />
                      {item.comment}
                      <HeartTwoTone
                        onClick={this.clickLikeComment}
                        style={{ float: "right" }}
                      />
                    </List.Item>
                  )}
                />
              )}
            </TabPane>
            <TabPane tab="Likes" key="likes"></TabPane>
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
