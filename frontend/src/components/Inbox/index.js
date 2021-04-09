import React from "react";
import { Affix, Button, message, Tabs } from "antd";
import {
  LikeOutlined,
  SolutionOutlined,
  InfoCircleOutlined,
  DeleteOutlined,
} from "@ant-design/icons";
import InboxPost from "../InboxPost";
import InboxRequest from "../InboxRequest";
import InboxLike from "../InboxLike";
import { clearInbox } from "../../requests/requestInbox";
const { TabPane } = Tabs;

export default class Inbox extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      authorID: this.props.authorID,
    };
  }

  clickClearInbox = () => {
    clearInbox({ authorID: this.state.authorID }).then((res) => {
      if (res.status === 200) {
        message.success("Clear inbox successfully!");
      }
    });
  };

  render() {
    const { authorID } = this.state;

    return (
      <div>
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
        <Affix offsetTop={100}>
          <Button onClick={this.clickClearInbox}>
            <DeleteOutlined /> Clean Inbox
          </Button>
        </Affix>
      </div>
    );
  }
}
