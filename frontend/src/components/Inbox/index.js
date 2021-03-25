import React from "react";
import { Layout, Tabs } from "antd";
import {
  CommentOutlined,
  LikeOutlined,
  SolutionOutlined,
  InfoCircleOutlined,
} from "@ant-design/icons";
import InboxPost from "../InboxPost";
import InboxRequest from "../InboxRequest";
import InboxLike from '../InboxLike';
const { TabPane } = Tabs;
const { Content } = Layout;

export default class Inbox extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      authorID: "",
    };
  }

  componentDidMount() {
    this._isMounted = true;

    if (this.state.authorID === "" && this._isMounted) {
      this.setState({ authorID: this.props.authorID });
    }
  }

  render() {
    const { authorID } = this.state;

    return (
      <Layout>
        {/* <TopNav /> */}
        <Content style={{}}>
          <Tabs defaultActiveKey="Posts" tabPosition="left">
            <TabPane
              tab={
                <span>
                  <SolutionOutlined />
                  Posts
                </span>
              }
              key={"posts"}
            >
              <InboxPost authorID={authorID} />
            </TabPane>
            <TabPane
              tab={
                <span>
                  <CommentOutlined />
                  Comments
                </span>
              }
              key={"comments"}
            >
              ...
            </TabPane>
            <TabPane
              tab={
                <span>
                  <LikeOutlined />
                  Likes
                </span>
              }
              key={"likes"}
            >
              <InboxLike authorID={authorID} />
            </TabPane>
            <TabPane
              tab={
                <span>
                  <InfoCircleOutlined />
                  Requests
                </span>
              }
              key={"requests"}
            >
              <InboxRequest authorID={authorID} />
            </TabPane>
          </Tabs>
        </Content>
      </Layout>
    );
  }
}
