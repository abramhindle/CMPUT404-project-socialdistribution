import React from "react";
import { Button, Descriptions, message } from "antd";
import { getAuthorByUsername } from "../../requests/requestAuthor";
import ProfileChange from "../ProfileChange";
import GitHubCalendar from "react-github-calendar";
import { GithubOutlined } from "@ant-design/icons";

export default class Profile extends React.Component {
  constructor(props) {
    super(props);
    this._isMounted = false;
    this.state = {
      authorID: this.props.authorID,
      username: this.props.username,
      displayName: this.props.displayName,
      github: this.props.github,
      isModalVisible: false,
    };
  }

  updateDisplay() {
    if (!this.state.username) {
      // Either we can found username from state(props) or cookies or it is impossible to know
      const usernameFromCookies = localStorage.getItem("username");
      if (usernameFromCookies) {
        this.setState({username: usernameFromCookies});
      }
    }
    if (!this.state.authorID) {
      // Either we can found authorID from state(props) or cookies or it is impossible to know
      const authorIDFromCookies = localStorage.getItem("authorID");
      if (authorIDFromCookies) {
        this.setState({authorID: authorIDFromCookies});
      }
    }
    if (this.state.username) {
      getAuthorByUsername({username: this.state.username}).then(response => {
        if (response.status === 200) {
          if(Object.keys(response.data).length === 1) {
            message.error(response.data.msg);
          } else {
            localStorage.setItem("displayName", response.data.displayName);
            localStorage.setItem("github", response.data.github);
            this.setState({
              displayName: response.data.displayName,
              github: response.data.github
            });
          }
        }
      })
    }
  }

  componentDidMount() {
    this.updateDisplay();
  }

  handleClick = () => {
    this.setState({ isModalVisible: !this.state.isModalVisible });
  };

  handleChangeModalVisibility = () => {
    this.setState({ isModalVisible: !this.state.isModalVisible });
    this.updateDisplay();
  };

  render() {
    return (
      <div style={{ margin: "5% 20%", textAlign: "center" }}>
        <Descriptions title="User Info">
          <Descriptions.Item label="UserName">
            {this.state.username}
          </Descriptions.Item>
          <Descriptions.Item label="displayName">
            {this.state.displayName}
          </Descriptions.Item>
          <Descriptions.Item label="github">
            {this.state.github}
          </Descriptions.Item>
        </Descriptions>
        {/* change info */}
        <Button
          type="primary"
          onClick={this.handleClick}
          style={{ width: "120px" }}
        >
          Change Info
        </Button>
        {/* logout */}
        <Button
          type="primary"
          danger
          onClick={this.props.logout}
          style={{ marginLeft: "100px", width: "120px" }}
        >
          Logout
        </Button>
        <ProfileChange
          authorID={this.props.authorID}
          displayName={this.state.displayName}
          github={this.state.github}
          visible={this.state.isModalVisible}
          handleChangeModalVisibility={this.handleChangeModalVisibility}
        />
        <div style={{ marginTop: "5%" }}>
          <GithubOutlined />
          <Descriptions title="My Github Activity"></Descriptions>
          <GitHubCalendar
            username={
              /([a-zA-Z0-9_-])+(?!.*[a-zA-Z0-9_-]+)/.exec(this.state.github)[0]
            }
            years={[2021]}
            blockMargin={5}   
          />
        </div>
      </div>
    );
  }
}
