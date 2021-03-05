import React from "react";
import { message, Avatar, Button, Card, List, Divider, Popover } from "antd";
import { UserOutlined, LikeOutlined, DislikeOutlined, UserAddOutlined } from "@ant-design/icons";
import CommentArea from "../CommentArea";
import { getCommentList } from "../../requests/requestComment";
import { postRequest } from "../../requests/requestFriendRequest";
import EditPostArea from "../EditPostArea";

export default class PostDisplay extends React.Component {
  constructor(props) {
    super(props);
    this._isMounted = false;
    this.state = {
      isModalVisible: false,
      isEditModalVisible: false,
      authorID: "",
    };
  }



  componentDidMount() {
    if (this.state.authorID === "") {
      this.setState({ authorID: this.props.authorID });
    }
    getCommentList({ postID: this.props.postID }).then((res) => {
      if (res.status === 200) {
        this.setState({ comments: res.data });
      }
    });
  }


  handleClickFollow = async () => {
    var n = this.props.postID.indexOf("/post/")
    let params = {
      actor: this.props.authorID,
      object: this.props.postID.substring(0,n),
      summary: "I want to follow you!",
    };
    postRequest(params).then((response) => {
      if (response.status === 200){
        message.success("Request sent!");
          window.location.reload();
        } else {
          message.error("Request failed!");
        }

    });
  }

  handleClickReply = () => {
    this.setState({ isModalVisible: !this.state.isModalVisible });
  };

  handleClickEdit = () => {
    this.setState({ isEditModalVisible: !this.state.isEditModalVisible });
  };

  handleCommentModalVisiblility = () => {
    this.setState({ isModalVisible: !this.state.isModalVisible });
  };

  handleEditPostModalVisiblility = () => {
    this.setState({ isModalVisible: !this.state.isModalVisible });
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
      github,
      content,
      datetime,
      postID,
      enableEdit,
    } = this.props;
    const content1 = (
      <div>
        <p>{authorName}</p>
        <p>{github}</p>
        <Button icon={<UserAddOutlined />} onClick={this.handleClickFollow} />
      </div>
    );
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

    return (
      <div>
        <Card
          title={title}
          extra={
            <span>
              <Popover content={content1} title="User Info" trigger="click">
                <Button icon={<UserOutlined />} 
                />
              </Popover>
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
        </Card>
      </div>
    );
  }
}
