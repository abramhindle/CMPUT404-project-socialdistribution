import React from "react";
import { Form, Input, Button, Checkbox, Tabs, message } from "antd";
import Signup from "../Signup";
import { getAuthor } from "../../requests/requestAuthor";
import { domain, port } from "../../requests/URL";

const { TabPane } = Tabs;

const layout = {
  labelCol: { span: 8 },
  wrapperCol: { span: 16 },
};

const tailLayout = {
  wrapperCol: { offset: 8, span: 16 },
};

export default class LoginComp extends React.Component {
  _isMounted = false;
  state = {
    autoLogin: true,
  };

  onFinish = (values) => {
    getAuthor(values).then((response) => {
      if (response.status === 400) {
        message.error(response.data.non_field_errors);
      } else if (response.status === 200) {
        localStorage.setItem("token", response.data.token);
        //fetch user and author
        fetch(`${domain}:${port}/current-user/`, {
          headers: {
            Authorization: `JWT ${localStorage.getItem("token")}`,
          },
        })
          .then((res) => res.json())
          .then((json) => {
            localStorage.setItem("username", json.username);
            // get author
            fetch(`${domain}:${port}/user-author/`, {
              headers: {
                Authorization: `JWT ${localStorage.getItem("token")}`,
              },
            })
              .then((res) => res.json())
              .then((json) => {
                localStorage.setItem("authorID", json.id);
                localStorage.setItem("displayName", json.displayName);
                localStorage.setItem("github", json.github);
                window.location.reload();
              });
          });
      } else {
        message.error("Unknown error.");
      }
    });
  };

  render() {
    return (
      <div
        style={{
          width: "330px",
          marginTop: "128px",
          marginLeft: "auto",
          marginRight: "auto",
        }}
      >
        <Tabs defaultActiveKey="login" centered>
          <TabPane tab="Login" key="login">
            <Form
              {...layout}
              name="login"
              initialValues={{ remember: true }}
              onFinish={this.onFinish}
            >
              <Form.Item
                label="Username"
                name="username"
                rules={[
                  { required: true, message: "Please input your username!" },
                ]}
              >
                <Input />
              </Form.Item>

              <Form.Item
                label="Password"
                name="password"
                rules={[
                  { required: true, message: "Please input your password!" },
                ]}
              >
                <Input.Password />
              </Form.Item>

              <Form.Item
                {...tailLayout}
                name="remember"
                valuePropName="checked"
              >
                <Checkbox>Remember me</Checkbox>
              </Form.Item>

              <Form.Item {...tailLayout}>
                <Button type="primary" htmlType="submit">
                  Submit
                </Button>
              </Form.Item>
            </Form>
          </TabPane>
          {/* registration */}
          <TabPane tab="Sign up" key="signup">
            <Signup />
          </TabPane>
        </Tabs>
      </div>
    );
  }
}
