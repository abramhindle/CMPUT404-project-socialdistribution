import React from "react";
import { List, message, Image } from "antd";
import { getAuthorUseID } from "../../requests/requestAuthor";
import {getInboxPost} from "../../requests/requestPost";
import { domain, port } from "../../requests/URL";
import ReactMarkdown from "react-markdown";
import PostDisplay from "../PostDisplay";

export default class InboxPost extends React.Component {
  constructor(props) {
    super(props);
    this._isMounted = false;
    this.state = {
      postData: [],
      postDataSet: [],
      authorID: this.props.authorID,
    };
  }

  componentDidMount() {
    this._isMounted = true;
    if (this.state.authorID === undefined || this.state.authorID === "") {
      // get author
      fetch(`${domain}:${port}/user-author/`, {
        headers: {
          Authorization: `JWT ${localStorage.getItem("token")}`,
        },
      })
        .then((res) => res.json())
        .then((json) => {
          this.setState({
            authorID: json.id,
          });
        });
    } else {
      console.log("stream1", this.state.authorID);
      getInboxPost({
        authorID: this.state.authorID,
      }).then((res) => {
        if (res.status === 200) {
          const publicPosts = this.getPostDataSet(res.data);
          this.setState({ myPostDataSet: publicPosts });
        } else {
          message.error("Fail to get my posts.");
        }
      });
    }
  }

  componentWillUnmount() {
    this._isMounted = false;
  }

  getPostDataSet = (postData) => {
    var publicPosts = [];
    postData.forEach((element) => {
      let contentHTML = <p>{element.content}</p>;
      const isImage =
        element.contentType.slice(0, 5) === "image" ? true : false;
      const isMarkDown =
        element.contentType.slice(5) === "markdown" ? true : false;
      if (isImage) {
        contentHTML = <Image width={150} src={element.content} />;
      } else if (isMarkDown) {
        contentHTML = <ReactMarkdown source={element.content} />;
      }

      const post = {
        title: element.title,
        content: <div style={{ margin: "24px" }}>{contentHTML}</div>,
        datetime: <span>{element.published}</span>,
        postID: element.id,
      };
      // TODO: can't show author name
      getAuthorUseID({ authorID: element.author }).then((res) => {
        post.authorName = res.data.displayName;
        post.github = res.data.github;
      });
      publicPosts.push(post);
    });
    this.setState({ postDataSet: publicPosts });
  };

  render() {
    const { postDataSet } = this.state;
    console.log("inboxpost", this.props.authorID);
    return (
      <div style={{}}>
        <List
          className="posts-list"
          itemLayout="horizontal"
          dataSource={postDataSet}
          renderItem={(item) => (
            <li>
              <PostDisplay
                title={item.title}
                authorName={item.authorName}
                github={item.github}
                content={item.content}
                datetime={item.datetime}
                authorID={this.props.authorID}
                postID={item.postID}
              />
            </li>
          )}
        />
      </div>
    );
  }
}
