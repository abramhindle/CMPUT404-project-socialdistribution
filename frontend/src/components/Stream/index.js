import React from "react";
import { List, message, Image, Input } from "antd";
import { getAllPublicPosts } from "../../requests/requestPost";
import { getAuthorUseID } from "../../requests/requestAuthor";
import ReactMarkdown from "react-markdown";
import PostDisplay from "../PostDisplay";

export default class Stream extends React.Component {
  constructor(props) {
    super(props);
    this._isMounted = false;
    this.state = {
      postData: [],
      postDataSet: [],
    };
  }

  componentDidMount() {
    this._isMounted = true;
    getAllPublicPosts().then((res) => {
      if (res.status === 200) {
        this.setState({ postData: res.data });
        this.getPostDataSet(res.data);
      } else {
        message.error("Fail to get all public posts.");
      }
    });
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
      });
      publicPosts.push(post);
    });
    this.setState({ postDataSet: publicPosts });
  };

  render() {
    const { postDataSet } = this.state;
    console.log("steam", this.props.authorID);
    return (
      <div style={{ margin: "10% 20%" }}>
        <List
          className="posts-list"
          itemLayout="horizontal"
          dataSource={postDataSet}
          renderItem={(item) => (
            <li>
              <PostDisplay
                title={item.title}
                authorName={item.authorName}
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
