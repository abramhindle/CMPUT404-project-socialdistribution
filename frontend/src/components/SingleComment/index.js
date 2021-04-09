import React from "react";
import { message } from "antd";
import { HeartTwoTone } from "@ant-design/icons";
import {
  sendLikes,
  getLikes,
  getRemoteLikes,
  sendRemoteLikes,
} from "../../requests/requestLike";
import { getDomainName, getLikeDataSet } from "../Utils";
import { domainAuthPair } from "../../requests/URL";
import { sendToInbox, sendToRemoteInbox } from "../../requests/requestInbox";

export default class CommentItem extends React.Component {
  state = {
    authorID: this.props.item.actor,
    isLiked: false,
    likesList: [],
    num: 0,
  };

  componentDidMount() {
    const domain = getDomainName(this.props.item.commentid);
    if (domain !== window.location.hostname) {
      getRemoteLikes({
        URL: `${this.props.item.commentid}/likes/`,
        auth: domainAuthPair[getDomainName(this.props.item.commentid)],
      }).then((res) => {
        if (res.status === 200) {
          getLikeDataSet(res.data).then((val) => {
            const likesNum = val.length + this.state.num;
            this.setState({ likesList: val, num: likesNum });
            this.state.likesList.forEach((item) => {
              if (item.authorID === this.state.authorID) {
                this.setState({ isLiked: true });
              }
            });
          });
        } else {
          message.error("Remote: Request failed!");
        }
      });
    } else {
      getLikes({ _object: this.props.item.commentid }).then((res) => {
        if (res.status === 200) {
          getLikeDataSet(res.data).then((val) => {
            const likesNum = val.length + this.state.num;
            this.setState({ likesList: val, num: likesNum });
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
  }

  clickLikeComment = (item) => {
    if (this.state.isLiked === false) {
      this.setState({
        isLiked: true,
      });
      let params = {
        authorID: this.props.item.authorID,
        type: "Like",
        postID: this.props.item.postID,
        actor: this.props.item.actor,
        object: this.props.item.commentid,
        summary: "I like your comment!",
        context: this.props.item.postID,
      };

      const commentIDDomain = getDomainName(this.props.item.commentid);
      if (commentIDDomain !== window.location.hostname) {
        params.URL = `${this.props.item.commentid}/likes/`;
        params.auth = domainAuthPair[getDomainName(params.URL)];
        params.author = this.state.authorID;
        sendRemoteLikes(params).then((response) => {
          if (response.status !== 200) {
            message.error("Likes remote send failed!");
          }
        });
      } else {
        sendLikes(params).then((response) => {
          if (response.status === 200) {
            message.success("Comment Likes sent!");
          } else {
            message.error("Send Comment Likes failed!");
          }
        });
      }
      const commentAuthorDomain = getDomainName(this.props.item.authorID);
      if (commentAuthorDomain !== window.location.hostname) {
        params.auth = domainAuthPair[commentAuthorDomain];
        sendToRemoteInbox(params).then((response) => {
          if (response.status !== 200) {
            message.error("Likes remote inbox send failed!");
          }
        });
      } else {
        sendToInbox(params).then((response) => {
          if (response.status !== 200) {
            message.error("Send Inbox Likes failed!");
          }
        });
      }
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
