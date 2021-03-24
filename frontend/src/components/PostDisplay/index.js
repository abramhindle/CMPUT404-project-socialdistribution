import React from "react";
import { message, Avatar, Button, Card, List, Divider, Popover } from "antd";
import {
  UserOutlined,
  UserAddOutlined,
  HeartTwoTone,
} from "@ant-design/icons";

import CommentArea from "../CommentArea";
import { getCommentList } from "../../requests/requestComment";
import { postRequest } from "../../requests/requestFriendRequest";
import EditPostArea from "../EditPostArea";
import ConfirmModal from "../ConfirmModal";
import { deletePost } from "../../requests/requestPost";
import {getLikes,sendLikes} from "../../requests/requestLike"

export default class PostDisplay extends React.Component {
  state = {
    comments: [],
    isModalVisible: false,
    isEditModalVisible: false,
    isDeleteModalVisible: false,
    authorID: this.props.authorID,
    isLiked:false,
    likesList:[],
  };

  componentDidMount() {
    getCommentList({ postID: this.props.postID }).then((res) => {
      if (res.status === 200) {
        this.setState({ comments: res.data });
      }
    });
    getLikes({_object : this.props.postID}).then((res) => {
      if (res.status === 200) {
        this.setState({ likesList:res.data });
        this.state.likesList.forEach((item)=>{
          if (item.author_id === this.state.authorID){
            this.setState({isLiked:true})
          }
        })
      }else {
        message.error("Request failed!");
      };
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
      } else {
        message.error("Request failed!");
      }
    });
  };

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

  handlelike= () => {
    getLikes({_object : this.props.postID}).then((res) => {
      if (res.status === 200) {
        this.setState({ likesList:res.data });
        console.log(this.state.likesList) 
      }else {
        message.error("Request failed!");
      };
    });
    
  };

  handleClickLike = () => {
    if (this.state.isLiked === false) {
      this.setState({
        isLiked:true
      });
        
    
      let params = {
        postID: this.props.postID,
        actor: this.props.authorID,
        object: this.props.postID.substring,
        summary: "I like you post!",
        context: this.props.postID,
      };
      sendLikes(params).then((response) => {
      if (response.status === 200){
        message.success("Request sent!");
        } else {
          message.error("Request failed!");
        };
      });
  }
  else{
    this.setState.isLiked = true;
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
      enableEdit,
    } = this.props;

    const content1 = (
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
    // postID = this.props.postID
    // actor = this.props.authorID
    
    const likeIconColor = this.state.isLiked? "#eb2f96":"#A5A5A5"
    return (
      <div>
        <Card
          title={title}
          extra={
            <span>
              <Popover content={content1} title="User Info" trigger="click">
                <Button icon={<UserOutlined />} />
              </Popover>
              <p>{authorName}</p>
            </span>
          }
        >
          <div style={{ margin: "24px", textAlign: "center" }}>{content}</div>
          <p>{datetime}</p>
          <div>
            <HeartTwoTone twoToneColor={likeIconColor} onClick={this.handleClickLike}/>

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
                {authorName}
                <p>{item.published}</p>
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
