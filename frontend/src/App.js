import React from "react";
import { BrowserRouter as Router, Route, Link } from "react-router-dom";
import { Layout, Avatar, Menu, Select, Drawer, Button, message } from "antd";
import {
  BookOutlined,
  UserOutlined,
  TeamOutlined,
  HomeOutlined,
  MailOutlined,
  UserAddOutlined,
} from "@ant-design/icons";
import "./App.css";
import PublicAndMyPost from "./components/PublicAndMyPost";
import Post from "./components/Post";
import Inbox from "./components/Inbox";
import Friends from "./components/Friends";
import Profile from "./components/Profile";
import LoginComp from "./components/LoginComp";
import { getAllAuthors } from "./requests/requestAuthor";
import { postRequest } from "./requests/requestFriendRequest";

const { Header, Content, Footer } = Layout;
const { Option } = Select;

export default class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      loggedIn: localStorage.getItem("token") ? true : false,
      authorID: localStorage.getItem("authorID"),
      username: localStorage.getItem("username"),
      displayName: localStorage.getItem("displayName"),
      github: localStorage.getItem("github"),
      authorList: [],
      objectID: undefined,
      authorValue: undefined,
      authorGithub: undefined,
      drawerVisible: false,
      currentTab: "/",
    };
    this._isMounted = false;
  }

  componentDidMount() {
    this._isMounted = true;
    if (this._isMounted) {
      this.setState({ currentTab: window.location.pathname });
    }
    if (this.state.loggedIn) {
      getAllAuthors().then((res) => {
        if (res.status === 200) {
          this.getAuthorDataSet(res.data).then((value) => {
            this.setState({ authorList: value });
          });
        } else {
          message.error("Request failed!");
        }
      });
    }
  }

  componentWillUnmount() {
    this._isMounted = false;
  }

  hide = () => {
    this.setState({
      drawerVisible: false,
    });
  };

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

  onChange = (value) => {
    var authorInfo = value.split(",");
    this.setState({
      authorValue: authorInfo[0],
      authorGithub: authorInfo[1],
      objectID: authorInfo[2],
      drawerVisible: true,
    });
  };

  handleClickFollow = async () => {
    let params = {
      actor: this.state.authorID,
      object: this.state.objectID,
      summary: "I want to follow you!",
    };
    postRequest(params).then((response) => {
      if (response.status === 200) {
        message.success("Request sent!");
        window.location.reload();
      } else if (response.status === 409) {
        message.error("Invalid request!");
      } else {
        message.error("Request failed!");
      }
    });
  };

  getAuthorDataSet = (authorData) => {
    let promise = new Promise(async (resolve, reject) => {
      const authorArray = [];
      for (const author of authorData) {
        authorArray.push({
          authorID: author.id,
          authorName: author.displayName,
          authorGithub: author.github,
        });
      }
      resolve(authorArray);
    });
    return promise;
  };

  render() {
    const {
      loggedIn,
      authorID,
      username,
      displayName,
      github,
      currentTab,
      authorValue,
      authorGithub,
    } = this.state;

    const options = this.state.authorList.map((d) => (
      <Option key={[d.authorName, d.authorGithub, d.authorID]}>
        {d.authorName}
      </Option>
    ));

    let content = loggedIn ? (
      <Layout className="layout">
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
            <Menu.Item className="modified-menu-item" key="/search">
              <Select
                showSearch
                style={{ width: 200, marginLeft: "24px" }}
                placeholder="Search for a user"
                optionFilterProp="children"
                onChange={this.onChange}
                filterOption={(input, option) =>
                  option.children.toLowerCase().indexOf(input.toLowerCase()) >=
                  0
                }
              >
                {options}
              </Select>
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
          <Drawer
            title="User Info"
            placement="right"
            closable={false}
            onClose={this.hide}
            visible={this.state.drawerVisible}
          >
            <Avatar icon={<UserOutlined />} />
            <p>{authorValue}</p>
            <p>{authorGithub}</p>
            <Button
              icon={<UserAddOutlined />}
              onClick={this.handleClickFollow}
            />
          </Drawer>
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
      <Route
        exact
        path="/"
        component={() => <LoginComp setCurrentTab={this.setCurrentTab} />}
      />
    );
    return <Router>{content}</Router>;
  }
}
