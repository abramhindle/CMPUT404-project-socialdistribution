import React from "react";
import { message, Avatar, Button, Card, List, Popover, Tag, Tabs } from "antd";
import { UserOutlined, UserAddOutlined, HeartTwoTone } from "@ant-design/icons";
import { getCommentList } from "../../requests/requestComment";
import { getAuthorByAuthorID } from "../../requests/requestAuthor";
import {
  getLikes,
  sendLikes,
  getCommentLikes,
} from "../../requests/requestLike";
    
export default class CommentItem extends React.Component {
    state = {
        authorID: this.props.item.actor,
        isLiked: false,
        likesList: [],
        num:0,
      };

  componentDidMount() {
    getCommentLikes({ _object: this.props.item.commentid }).then((res) => {
        if (res.status === 200) {
        this.getLikeDataSet(res.data).then((val) => {
            this.setState({ likesList: val, num:val.length});
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

  clickLikeComment = (item) => {
    console.log("item",this.props.item);
    if (this.state.isLiked === false) {
        this.setState({
          isLiked: true,
        });
      console.log("par",this.props)
      let params = {
        postID: this.props.item.postID,
        actor: this.props.item.actor,
        object: this.props.item.commentid,
        summary: "I like you comment!",
        context: this.props.item.postID,
      };
      console.log("params", params);
      sendLikes(params).then((response) => {
        if (response.status === 200) {
          message.success("Likes sent!");
        } else {
          message.error("Likes failed!");
        }
      });
    }else{
        this.setState.isLiked = true;
    }
  };
  
  render() {
    const likeIconColor = this.state.isLiked ? "#eb2f96" : "#A5A5A5";

    return (
      <div style={{ float: "right"}}>
      

            
    
        <HeartTwoTone
          twoToneColor={likeIconColor}
          onClick={this.clickLikeComment}
          
        />
        {this.state.num}
        
        
      </div>
    );
  }
}
