import React from "react";
import LoginComp from "../LoginComp";
import TopNav from "../TopNav";
import { Layout, Tabs } from "antd";
import Post from "../Post";

const { TabPane } = Tabs;
const { Content } = Layout;

export default class Home extends React.Component {
  state = {
    loggedIn: localStorage.getItem("token") ? true : false,
    authorID: "",
  };

  componentDidMount() {
    if (this.state.loggedIn) {
      fetch("http://localhost:8000/core/current_user/", {
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

  render() {
    const { loggedIn, authorID } = this.state;

    let content;
    if (loggedIn) {
      content = (
        <Layout>
          <TopNav />
          <Content>
            <Tabs defaultActiveKey="1" tabPosition={"left"}>
              <TabPane tab={"Profile"} key={1}>
                ...
              </TabPane>
              <TabPane tab={"Home"} key={2}>
                <Post authorID={authorID} />
              </TabPane>
              <TabPane tab={"Inbox"} key={3}>
                ...
              </TabPane>
              <TabPane tab={"Friend"} key={4}>
                ...
              </TabPane>
            </Tabs>
          </Content>
        </Layout>
      );
      content = <LoginComp />;
    } else {
      content = <LoginComp />;
    }
    return <div>{content}</div>;
  }
}
