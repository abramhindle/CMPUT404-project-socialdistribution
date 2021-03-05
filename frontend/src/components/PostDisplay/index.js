import React from "react";
import { message, Avatar, Button, Card, List, Divider, Popover } from "antd";
import {
  UserOutlined,
  LikeOutlined,
  DislikeOutlined,
  UserAddOutlined,
} from "@ant-design/icons";
import CommentArea from "../CommentArea";
import { getCommentList } from "../../requests/requestComment";
import { postRequest } from "../../requests/requestFriendRequest";
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
      likeslist:[],
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

  handleClickDislike = () => {
    //TODO
  };

  handleClickLike = () => {
    if (this.state.isLiked == false){
      this.setState((prevState)=>{console.log(prevState)
        return{
            isLiked:!prevState.isLiked,
            likeslist:[...this.state.likeslist,this.props.authorID],
        }
        },()=>{
        console.log(this.state.likeslist) 
        })
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
    
      }
    else {
      this.setState((prevState)=>{console.log(prevState)
      return{
          isLiked:!prevState.isLiked,
          likeslist:this.state.likeslist.splice(this.state.likeslist.find(item => item.value == this.props.authorID),1)
      }
      },()=>{
      console.log(this.state.likeslist) 
      })}
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
            <span onClick={() => this.handleClickLike()}>
                    {
                        this.state.isLiked ? '💓 Cancel' :'🖤 Like'
                    }
            </span>
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
