import React from "react";
import { Comment, Tooltip, List, message, Avatar } from "antd";
import { UserOutlined } from "@ant-design/icons";
import moment from "moment";
import { getAllPublicPosts } from "../../requests/requestPost";
import { getAuthorUseID } from "../../requests/requestAuthor";

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
      const post = {
        actions: [<span key="comment-list-reply-to-0">Reply to</span>],
        avatar: <Avatar icon={<UserOutlined />} />,
        content: <p>{element.content}</p>,
        datetime: <span>{element.published}</span>,
      };
      // TODO: can't show author name
      getAuthorUseID({ authorID: element.author }).then((res) => {
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
