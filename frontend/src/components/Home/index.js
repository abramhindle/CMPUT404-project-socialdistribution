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

const { TabPane } = Tabs;
const { Content } = Layout;

export default class Home extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      loggedIn: localStorage.getItem("token") ? true : false,
      authorID: "",
      username: "",
    };
    this.saveAuthorIDHome = this.saveAuthorIDHome.bind(this);
  }

  componentDidMount() {
    if (this.state.loggedIn) {
      fetch("http://localhost:8000/current-user/", {
        headers: {
          Authorization: `JWT ${localStorage.getItem("token")}`,
        },
      })
        .then((res) => res.json())
        .then((json) => {
          this.setState({ username: json.username });
        });
    }
  }

  saveAuthorIDHome(id) {
    this.setState({ authorID: id });
  }

  logout() {
    localStorage.removeItem("token");
    this.setState({ loggedIn: null, authorID: "" });
  }

  render() {
    const { loggedIn, authorID } = this.state;

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
                ...
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
                <Post authorID={authorID} />
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
                ...
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
                ...
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
