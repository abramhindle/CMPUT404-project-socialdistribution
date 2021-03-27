import React from "react";
import { List, message, Image } from "antd";
import { getAuthorByAuthorID } from "../../requests/requestAuthor";
import { getInboxPost } from "../../requests/requestPost";
import ReactMarkdown from "react-markdown";
import PostDisplay from "../PostDisplay";

export default class InboxPost extends React.Component {
  constructor(props) {
    super(props);
    this._isMounted = false;
    this.state = {
      postDataSet: [],
      authorID: this.props.authorID,
    };
  }

  componentDidMount() {
    this._isMounted = true;
    getInboxPost({
      authorID: this.state.authorID,
    }).then((res) => {
      if (res.status === 200) {
        this.getPostDataSet(res.data).then((value) => {
          this.setState({ postDataSet: value });
        });
      } else {
        message.error("Fail to get posts.");
      }
    });
  }

  componentWillUnmount() {
    this._isMounted = false;
  }

  getPostDataSet = (postData) => {
    let promise = new Promise(async (resolve, reject) => {
      const publicPosts = [];
      for (const element of postData) {
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

        const res = await getAuthorByAuthorID({ authorID: element.author });
        let rawPost = element;
        rawPost["authorName"] = res.data.displayName;
        publicPosts.push({
          title: element.title,
          content: <div style={{ margin: "24px" }}>{contentHTML}</div>,
          datetime: <span>{element.published}</span>,
          postID: element.id,
          authorName: res.data.displayName,
          github: res.data.github,
          categories: element.categories,
          rawPost: rawPost,
        });
      }
      resolve(publicPosts);
    });
    return promise;
  };

  render() {
    const { postDataSet } = this.state;

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
                authorID={this.state.authorID}
                postID={item.postID}
                rawPost={item.rawPost}
                categories={item.categories}
              />
            </li>
          )}
        />
      </div>
    );
  }
}
