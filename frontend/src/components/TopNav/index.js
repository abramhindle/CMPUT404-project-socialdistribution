import React from "react";
import { Menu } from "antd";
import Layout from "antd/lib/layout";
import { HomeOutlined, BookOutlined, ProfileOutlined } from "@ant-design/icons";

export default class TopNav extends React.Component {
  state = { current: "home" };

  handleClick = (e) => {
    console.log("click ", e);
    this.setState({ current: e.key });
  };

  render() {
    const { current } = this.state;

    return (
      <Layout className="layout">
        <Menu onClick={this.handleClick} selectedKeys={current}>
          <Menu.Item key="home" icon={<HomeOutlined />}>
            Home
          </Menu.Item>
          <Menu.Item key="home" icon={<BookOutlined />}>
            Post
          </Menu.Item>
          <Menu.Item key="home" icon={<ProfileOutlined />}>
            Profile
          </Menu.Item>
        </Menu>
      </Layout>
    );
  }
}
