import React from "react";
import { message } from "antd";
import { HeartTwoTone } from "@ant-design/icons";
import { getAuthorByAuthorID } from "../../requests/requestAuthor";
import { sendLikes, getLikes ,getRemoteLikes,sendRemoteLikes} from "../../requests/requestLike";

export default class CommentItem extends React.Component {
  state = {
    authorID: this.props.item.actor,
    isLiked: false,
    likesList: [],
    num: 0,
  };

  componentDidMount() {
    if (this.props.item.remote) {
        getRemoteLikes({
          URL: `${this.props.item.commentid}/likes/`,
          auth: this.props.remoteAuth,
        }).then((res) => {
          // console.log(res.data)
          if (res.status === 200) {
            this.getLikeDataSet(res.data).then((val) => {
              this.setState({ likesList: val });
              this.state.likesList.forEach((item) => {
                if (item.authorID === this.state.authorID) {
                  this.setState({ isLiked: true });
                }
              });
            });
          }else {
                message.error("Request remote comment like failed!");
        }
        });
      } else {
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
            message.error("Request comment like failed!");
          }
        });
      }
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
    if (this.state.isLiked === false) {
      this.setState({
        isLiked: true,
      });
      let params = {
        postID: this.props.item.postID,
        actor: this.props.item.actor,
        object: this.props.item.commentid,
        summary: "I like you comment!",
        context: this.props.item.postID,
      };
      sendLikes(params).then((response) => {
        if (response.status === 200) {
          message.success("Likes sent!");
          window.location.reload();
        } else {
          message.error("Likes failed!");
        }
      });
    } else {
      this.setState.isLiked = true;
    }
  };

  render() {
    const likeIconColor = this.state.isLiked ? "#eb2f96" : "#A5A5A5";

    return (
      <div style={{ float: "right" }}>
        <HeartTwoTone
          twoToneColor={likeIconColor}
          onClick={this.clickLikeComment}
        />{" "}
        {this.state.num}
      </div>
    );
  }
}
