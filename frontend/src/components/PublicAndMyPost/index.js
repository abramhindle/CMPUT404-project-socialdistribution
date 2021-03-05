import React from "react";
import { List, message, Image, Tabs } from "antd";
import { getAllPublicPosts, getPostList } from "../../requests/requestPost";
import { getAuthorUseID } from "../../requests/requestAuthor";
import ReactMarkdown from "react-markdown";
import PostDisplay from "../PostDisplay";
import { domain, port } from "../../requests/URL";

const { TabPane } = Tabs;

export default class PublicAndMyPost extends React.Component {
  constructor(props) {
    super(props);
    this._isMounted = false;
    this.state = {
      publicPostDataSet: [],
      myPostDataSet: [],
      authorID: this.props.authorID,
    };
    console.log("stream", this.props.authorID);
  }

  componentDidMount() {
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
      getPostList({
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
    getAllPublicPosts().then((res) => {
      if (res.status === 200) {
        const publicPosts = this.getPostDataSet(res.data);
        this.setState({ publicPostDataSet: publicPosts });
      } else {
        message.error("Fail to get my posts.");
      }
    });
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
    return publicPosts;
  };

  render() {
    const { publicPostDataSet, myPostDataSet } = this.state;
    return (
      <div style={{ margin: "10% 20%" }}>
        <Tabs defaultActiveKey="Posts">
          <TabPane tab={<span>Public Posts</span>} key={"posts"}>
            <List
              className="posts-list"
              itemLayout="horizontal"
              dataSource={publicPostDataSet}
              renderItem={(item) => (
                <li>
                  <PostDisplay
                    title={item.title}
                    authorName={item.authorName}
                    content={item.content}
                    datetime={item.datetime}
                    authorID={this.state.authorID}
                    postID={item.postID}
                  />
                </li>
              )}
            />
          </TabPane>
          <TabPane tab={<span>My Posts</span>} key={"comments"}>
            <List
              className="posts-list"
              itemLayout="horizontal"
              dataSource={myPostDataSet}
              renderItem={(item) => (
                <li>
                  <PostDisplay
                    title={item.title}
                    authorName={item.authorName}
                    content={item.content}
                    datetime={item.datetime}
                    authorID={this.state.authorID}
                    postID={item.postID}
                  />
                </li>
              )}
            />
          </TabPane>
        </Tabs>
      </div>
    );
  }
}
