import React from "react";
import { Comment, List, message, Avatar, Image } from "antd";
import { UserOutlined } from "@ant-design/icons";
import moment from "moment";
import { getAllPublicPosts } from "../../requests/requestPost";
import { getAuthorUseID } from "../../requests/requestAuthor";
import ReactMarkdown from "react-markdown";

export default class Stream extends React.Component {
  constructor(props) {
    super(props);
    this._isMounted = false;
    this.state = {
      authorID: this.props.authorID,
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
      }
      if (isMarkDown) {
        contentHTML = <ReactMarkdown source={element.content} />;
      }
      const post = {
        actions: [<span key="comment-list-reply-to-0">Reply to</span>],
        avatar: <Avatar icon={<UserOutlined />} />,
        content: contentHTML,
        datetime: <span>{element.published}</span>,
      };
      // TODO: can't show author name
      getAuthorUseID({ authorID: element.author }).then((res) => {
        console.log("test", res.data.displayName);
        post.author = res.data.displayName;
      });
      publicPosts.push(post);
    });
    this.setState({ postDataSet: publicPosts });
  };

  render() {
    const { authorID, postDataSet } = this.state;

    return (
      <div style={{ margin: "10% 20%" }}>
        <List
          className="posts-list"
          itemLayout="horizontal"
          dataSource={postDataSet}
          renderItem={(item) => (
            <li>
              <Comment
                actions={item.actions}
                author={item.author}
                avatar={item.avatar}
                content={item.content}
                datetime={item.datetime}
              />
            </li>
          )}
        />
      </div>
    );
  }
}
