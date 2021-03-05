import React from "react";
import { Layout, Tabs, Avatar } from "antd";
import {
  CommentOutlined,
  LikeOutlined,
  SolutionOutlined,
  InfoCircleOutlined
} from "@ant-design/icons";
import Stream from "../Stream";
import InboxPost from "../InboxPost";

const { TabPane } = Tabs;
const { Content } = Layout;

export default class Inbox extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      authorID: ""
    };
  }

  componentDidMount() {
    this._isMounted = true;

    if (this.state.authorID === "" && this._isMounted) {
        this.setState({ authorID: this.props.authorID });
    }
  }


  render() {
    const {authorID} = this.state;
    console.log("inbox.....", authorID);
    let content;
    return(
        <Layout>
            {/* <TopNav /> */}
            <Content style={{ width: "100%", margin: "24px 10%" }}>
            <Tabs defaultActiveKey="Posts">
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
                ...
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
                ...
                </TabPane>
            </Tabs>
            </Content>
        </Layout>
    );
  }
}
