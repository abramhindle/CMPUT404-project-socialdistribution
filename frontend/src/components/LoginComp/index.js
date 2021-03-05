import React from "react";
import { Form, Input, Button, Checkbox, Tabs, message } from "antd";
import Signup from "../Signup";
import { getAuthor } from "../../requests/requestAuthor";

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
    authorID: "",
    autoLogin: true,
    username: "",
    password: "",
  };

  onFinish = (values) => {
    getAuthor(values).then((response) => {
      if (response.status === 400) {
        message.error(response.data.non_field_errors);
      } else if (response.status === 200) {
        localStorage.setItem("token", response.data.token);
        message.success("Welcome back!");
        window.location.reload();
      } else {
        message.error("Unknown error.");
      }
    });
  };

  saveAuthorID = (id) => {
    this.setState({ authorID: id });
    this.props.saveAuthorIDHome(id);
  };

  render() {
    const { userName, autoLogin } = this.state;
    return (
      <div
        style={{
          width: "300px",
          marginTop: "36px",
        }}
      >
        <Tabs defaultActiveKey="login">
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
            <Signup saveAuthorID={this.saveAuthorID} />
          </TabPane>
        </Tabs>
      </div>
    );
  }
}
