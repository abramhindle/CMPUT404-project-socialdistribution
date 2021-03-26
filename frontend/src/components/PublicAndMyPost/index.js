import React from "react";
import { List, message, Image, Tabs } from "antd";
import { getAllPublicPosts, getPostList } from "../../requests/requestPost";
import { getAuthorByAuthorID } from "../../requests/requestAuthor";
import ReactMarkdown from "react-markdown";
import PostDisplay from "../PostDisplay";

const { TabPane } = Tabs;

export default class PublicAndMyPost extends React.Component {
  constructor(props) {
    super(props);
    this._isMounted = false;
    this.state = {
      publicPostDataSet: [],
      myPostDataSet: [],
      authorID: this.props.authorID,
      authorName: "",
    };
  }

  componentDidMount() {
    getAllPublicPosts().then((res) => {
      if (res === undefined) {
        message.warning("Loading...");
      } else if (res.status === 200) {
        this.getPostDataSet(res.data).then((value) => {
          this.setState({ publicPostDataSet: value });
        });
      } else {
        message.error("Fail to get public posts.");
      }
    });

    getPostList({
      authorID: this.state.authorID,
    }).then((res) => {
      if (res === undefined) {
        message.warning("Loading...");
      } else if (res.status === 200) {
        this.getPostDataSet(res.data).then((value) => {
          this.setState({ myPostDataSet: value });
        });
      } else {
        message.error("Fail to get my posts.");
      }
    });
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
        publicPosts.push({
          title: element.title,
          content: <div style={{ margin: "24px" }}>{contentHTML}</div>,
          datetime: <span>{element.published}</span>,
          postID: element.id,
          authorName: res.data.displayName,
          github: res.data.github,
          categories: element.categories,
          rawPost: element,
        });
      }
      resolve(publicPosts);
    });
    return promise;
  };

  render() {
    const { publicPostDataSet, myPostDataSet } = this.state;

    return (
      <div>
        <Tabs defaultActiveKey="public-posts" tabPosition="left">
          <TabPane tab={<span>Public Posts</span>} key={"public-posts"}>
            <List
              className="posts-list"
              itemLayout="horizontal"
              dataSource={publicPostDataSet}
              renderItem={(item) => {
                return (
                  <li>
                    <PostDisplay
                      title={item.title}
                      authorName={item.authorName}
                      github={item.github}
                      content={item.content}
                      datetime={item.datetime}
                      authorID={this.state.authorID}
                      postID={item.postID}
                      categories={item.categories}
                      enableEdit={false}
                      rawPost={item.rawPost}
                    />
                  </li>
                );
              }}
            />
          </TabPane>
          <TabPane tab={<span>My Posts</span>} key={"my-posts"}>
            <List
              className="posts-list"
              itemLayout="horizontal"
              dataSource={myPostDataSet}
              renderItem={(item) => {
                return (
                  <li>
                    <PostDisplay
                      title={item.title}
                      authorName={item.authorName}
                      github={item.github}
                      content={item.content}
                      datetime={item.datetime}
                      authorID={this.state.authorID}
                      postID={item.postID}
                      categories={item.categories}
                      enableEdit={true}
                      rawPost={item.rawPost}
                    />
                  </li>
                );
              }}
            />
          </TabPane>
        </Tabs>
      </div>
    );
  }
}
