import React from "react";
import { List, message, Tabs } from "antd";
import {
  getAllPublicPosts,
  getAllRemotePublicPosts,
  getPostList,
} from "../../requests/requestPost";
import PostDisplay from "../PostDisplay";
import { auth, auth4, remoteDomain, remoteDomain4 } from "../../requests/URL";
import { getPostDataSet } from "../Utils";

const { TabPane } = Tabs;

export default class PublicAndMyPost extends React.Component {
  constructor(props) {
    super(props);
    this._isMounted = false;
    this.state = {
      publicPostDataSet: [],
      remotePublicPostDataSet: [],
      myPostDataSet: [],
      authorID: this.props.authorID,
      authorName: "",
    };
  }

  componentDidMount() {
    this._isMounted = true;
    // Our server
    getAllPublicPosts().then((res) => {
      if (res === undefined) {
        message.warning("Loading...");
      } else if (res.status === 200) {
        getPostDataSet(res.data).then((value) => {
          if (this._isMounted) {
            this.setState({ publicPostDataSet: value });
          }
        });
      } else {
        message.error("Fail to get public posts.");
      }
    });
    // Remote serveer
    getAllRemotePublicPosts({
      // URL: `${remoteDomain4}/posts/`,
      // auth: auth4,
      URL: `${remoteDomain}/post-list/`,
      auth: auth,
    }).then((res) => {
      if (res === undefined) {
        message.warning("Loading...");
      } else if (res.status === 200) {
        getPostDataSet(res.data).then((value) => {
          if (this._isMounted) {
            this.setState({ remotePublicPostDataSet: value });
          }
        });
      } else {
        message.error("Fail to get public posts.");
      }
    });
    // My post
    getPostList({
      authorID: this.state.authorID,
    }).then((res) => {
      if (res === undefined) {
        message.warning("Loading...");
      } else if (res.status === 200) {
        getPostDataSet(res.data).then((value) => {
          if (this._isMounted) {
            this.setState({ myPostDataSet: value });
          }
        });
      } else {
        message.error("Fail to get my posts.");
      }
    });
  }

  componentWillUnmount() {
    this._isMounted = false;
  }

  render() {
    const {
      publicPostDataSet,
      myPostDataSet,
      remotePublicPostDataSet,
    } = this.state;

    const combinedPublicPostDataSet = publicPostDataSet.concat(
      remotePublicPostDataSet
    );

    return (
      <div>
        <Tabs defaultActiveKey="public-posts" tabPosition="left">
          <TabPane tab={<span>Public Posts</span>} key={"public-posts"}>
            <List
              className="posts-list"
              itemLayout="horizontal"
              dataSource={combinedPublicPostDataSet}
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
                      remote={item.remote}
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
