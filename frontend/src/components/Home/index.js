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
import { domain, port } from "../../requests/URL";
import Stream from "../Stream";

const { TabPane } = Tabs;
const { Content } = Layout;

export default class Home extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      loggedIn: localStorage.getItem("token") ? true : false,
      authorID: "",
      username: "",
      displayName: "",
      github: "",
    };
  }

  componentDidMount() {
    if (this.state.loggedIn) {
      //get user
      fetch(`${domain}:${port}/current-user/`, {
        headers: {
          Authorization: `JWT ${localStorage.getItem("token")}`,
        },
      })
        .then((res) => res.json())
        .then((json) => {
          console.log("current_user", json);
          this.setState({ username: json.username });
        });
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
            displayName: json.displayName,
            github: json.github,
          });
        });
    }
  }

  saveAuthorIDHome = (id) => {
    this.setState({ authorID: id });
  };

  logout = () => {
    localStorage.removeItem("token");
    this.setState({ loggedIn: null, authorID: "" });
  };

  render() {
    const { loggedIn, authorID, username, displayName, github } = this.state;
    console.log("home", loggedIn, authorID);
    let content;
    if (loggedIn) {
      content = (
        <Layout>
          {/* <TopNav /> */}
          <Content style={{ width: "100%", margin: "24px 10%" }}>
            <Tabs defaultActiveKey="Home">
              <TabPane
                tab={
                  <span>
                    <HomeOutlined />
                    Home
                  </span>
                }
                key={"home"}
              >
                <Stream authorID={authorID} />
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
                <Post authorID={authorID} username={username} />
              </TabPane>
              <TabPane
                tab={
                  <span>
                    <MailOutlined />
                    Inbox
                  </span>
                }
                key={"inbox"}
              >
                ...
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
