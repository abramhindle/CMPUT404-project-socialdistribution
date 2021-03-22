import React from "react";
import LoginComp from "../LoginComp";
import { Layout, Tabs, Avatar } from "antd";
import {
  BookOutlined,
  UserOutlined,
  TeamOutlined,
  HomeOutlined,
  MailOutlined,
} from "@ant-design/icons";
import Post from "../Post";
import Profile from "../Profile";
import Friends from "../Friends";
import PublicAndMyPost from "../PublicAndMyPost";
import Inbox from "../Inbox";

const { TabPane } = Tabs;
const { Content } = Layout;

export default class Home extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      loggedIn: localStorage.getItem("token") ? true : false,
      authorID: localStorage.getItem("authorID"),
      username: localStorage.getItem("username"),
      displayName: localStorage.getItem("displayName"),
      github: localStorage.getItem("github"),
    };
  }

  logout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("username");
    localStorage.removeItem("authorID");
    localStorage.removeItem("displayName");
    localStorage.removeItem("github");
    this.setState({ loggedIn: null, authorID: "" });
  };

  render() {
    const { loggedIn, authorID, username, displayName, github } = this.state;

    let content;
    if (loggedIn) {
      content = (
        <Layout>
          {/* <TopNav /> */}
          <Content
            style={{
              marginTop: "24px",
              marginLeft: "15%",
              marginRight: "15%",
            }}
          >
            <Tabs defaultActiveKey="Home" centered>
              <TabPane
                tab={
                  <span>
                    <HomeOutlined />
                    Home
                  </span>
                }
                key={"home"}
              >
                <PublicAndMyPost authorID={authorID} />
              </TabPane>
              <TabPane
                tab={
                  <span>
                    <BookOutlined />
                    Write a Post
                  </span>
                }
                key={"post"}
              >
                <Post
                  authorID={authorID}
                  username={username}
                  enableEdit={false}
                />
              </TabPane>
              <TabPane
                tab={
                  <span>
                    <MailOutlined />
                    My Inbox
                  </span>
                }
                key={"inbox"}
              >
                <Inbox authorID={authorID} />
              </TabPane>
              <TabPane
                tab={
                  <span>
                    <TeamOutlined />
                    Friends
                  </span>
                }
                key={"friend"}
              >
                <Friends authorID={authorID} />
              </TabPane>
              <TabPane
                tab={
                  <span>
                    <Avatar
                      style={{ backgroundColor: "#87d068" }}
                      icon={<UserOutlined />}
                    />
                    <p style={{ display: "inline", marginLeft: "16px" }}>
                      {this.state.displayName}
                    </p>
                  </span>
                }
                key={"profile"}
                style={{ float: "right" }}
              >
                <Profile
                  authorID={authorID}
                  username={username}
                  displayName={displayName}
                  github={github}
                  logout={this.logout}
                />
              </TabPane>
            </Tabs>
          </Content>
        </Layout>
      );
      // content = <LoginComp />;
    } else {
      content = <LoginComp saveAuthorIDHome={this.saveAuthorIDHome} />;
    }
    return <div>{content}</div>;
  }
}
