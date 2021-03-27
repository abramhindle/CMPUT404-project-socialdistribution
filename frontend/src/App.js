import React from "react";
import { BrowserRouter as Router, Route, Link } from "react-router-dom";
import { Layout, Avatar, Menu } from "antd";
import {
  BookOutlined,
  UserOutlined,
  TeamOutlined,
  HomeOutlined,
  MailOutlined,
} from "@ant-design/icons";
import "./App.css";
import PublicAndMyPost from "./components/PublicAndMyPost";
import Post from "./components/Post";
import Inbox from "./components/Inbox";
import Friends from "./components/Friends";
import Profile from "./components/Profile";
import LoginComp from "./components/LoginComp";

const { Header, Content, Footer } = Layout;

export default class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      loggedIn: localStorage.getItem("token") ? true : false,
      authorID: localStorage.getItem("authorID"),
      username: localStorage.getItem("username"),
      displayName: localStorage.getItem("displayName"),
      github: localStorage.getItem("github"),
      currentTab: "/",
    };
    this._isMounted = false;
  }

  componentDidMount() {
    this._isMounted = true;
    if (this._isMounted) {
      this.setState({ currentTab: window.location.pathname });
    }
  }

  componentWillUnmount() {
    this._isMounted = false;
  }

  logout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("username");
    localStorage.removeItem("authorID");
    localStorage.removeItem("displayName");
    localStorage.removeItem("github");
    this.setState({ loggedIn: null, authorID: "" });
    window.location.href = "/";
  };

  clickNavBar = (e) => {
    this.setState({ currentTab: e.key });
  };

  render() {
    const {
      loggedIn,
      authorID,
      username,
      displayName,
      github,
      currentTab,
    } = this.state;

    let content = loggedIn ? (
      <Layout className="layout">
        {/* <TopNav /> */}
        <Header style={{ position: "fixed", zIndex: 1, width: "100%" }}>
          <Menu
            theme="dark"
            onClick={this.clickNavBar}
            selectedKeys={[currentTab]}
            mode="horizontal"
          >
            <Menu.Item key="/">
              <span>
                <HomeOutlined />
                Home
              </span>
              <Link to="/" />
            </Menu.Item>
            <Menu.Item key="/write-post">
              <span>
                <BookOutlined />
                Write a Post
              </span>
              <Link to="/write-post" />
            </Menu.Item>
            <Menu.Item key="/my-inbox">
              <span>
                <MailOutlined />
                My Inbox
              </span>
              <Link to="/my-inbox" />
            </Menu.Item>
            <Menu.Item key="/my-friends">
              <span>
                <TeamOutlined />
                Friends
              </span>
              <Link to="/my-friends" />
            </Menu.Item>
            <Menu.Item key="/my-profile" style={{ float: "right" }}>
              <span>
                <Avatar icon={<UserOutlined />} />
                <p style={{ display: "inline", marginLeft: "16px" }}>
                  {this.state.displayName}
                </p>
              </span>
              <Link to="/my-profile" />
            </Menu.Item>
          </Menu>
        </Header>
        <Content
          style={{
            minHeight: "1000px",
            marginTop: "100px",
            marginLeft: "15%",
            marginRight: "15%",
          }}
        >
          <Route
            exact
            path="/"
            component={() => <PublicAndMyPost authorID={authorID} />}
          />
          <Route
            path="/write-post"
            component={() => (
              <Post
                authorID={authorID}
                username={username}
                enableEdit={false}
              />
            )}
          />
          <Route
            path="/my-inbox"
            component={() => <Inbox authorID={authorID} />}
          />
          <Route
            path="/my-friends"
            component={() => <Friends authorID={authorID} />}
          />
          <Route
            path="/my-profile"
            component={() => (
              <Profile
                authorID={authorID}
                username={username}
                displayName={displayName}
                github={github}
                logout={this.logout}
              />
            )}
          />
        </Content>
        <Footer style={{ textAlign: "center" }}>
          CMPUT404-T1-Social-Distribution ©2022 Created by Bowei Li, Xuechun
          Qiu, Weida Wang, Zihao Huang, Zijian Xi
        </Footer>
      </Layout>
    ) : (
      <LoginComp setCurrentTab={this.setCurrentTab} />
    );
    return <Router>{content}</Router>;
  }
}
