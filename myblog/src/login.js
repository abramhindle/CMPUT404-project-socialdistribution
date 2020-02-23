import React from "react";
import "antd/dist/antd.css";
import "./index.css";
import "ant-design-pro/dist/ant-design-pro.css";
import Login from "ant-design-pro/lib/Login";
import { Alert, Checkbox } from "antd";
import "./CSS/login.css"
// using ES6 modules
import { BrowserRouter, Route, Link } from 'react-router-dom'//推荐使用

// using CommonJS modules
const BrowserRouter = require('react-router-dom').BrowserRouter
const Route = require('react-router-dom').Route
const Link = require('react-router-dom').Link

const { Tab, UserName, Password, Submit } = Login;

class LoginPage extends React.Component {
  state = {
    notice: "",
    type: "tab1",
    autoLogin: true
  };
  onSubmit = (err, values) => {
    console.log("value collected ->", {
      ...values,
      autoLogin: this.state.autoLogin
    });
    if (this.state.type === "tab1") {
      this.setState(
        {
          notice: ""
        },
        () => {
          if (
            !err &&
            (values.username !== "admin" || values.password !== "888888")
          ) {
            setTimeout(() => {
              this.setState({
                notice: "The combination of username and password is incorrect!"
              });
            }, 500);
          }
        }
      );
    }
  };
  onTabChange = key => {
    this.setState({
      type: key
    });
  };
  changeAutoLogin = e => {
    this.setState({
      autoLogin: e.target.checked
    });
  };
  render() {
    return (
      <div className="login-warp">
        
        <Login
          defaultActiveKey={this.state.type}
          onTabChange={this.onTabChange}
          onSubmit={this.onSubmit}
        >
          <Tab key="tab1" tab="Account">
            {this.state.notice && (
              <Alert
                style={{ marginBottom: 24 }}
                message={this.state.notice}
                type="error"
                showIcon
                closable
              />
            )}
            <UserName name="username" />
            <Password name="password" />
          </Tab>

          <div>
            <Checkbox
              checked={this.state.autoLogin}
              onChange={this.changeAutoLogin}
            >
              Keep me logged in
            </Checkbox>
            <a style={{ float: "right" }} href="">
              Forgot password
            </a>
          </div>
          <Submit>Login</Submit>
          <div>
            <a href="./register.js">Register</a>
          </div>
        </Login>
      </div>
    );
  }
}

// ReactDOM.render(<LoginDemo />, document.getElementById("container"));
export default LoginPage;