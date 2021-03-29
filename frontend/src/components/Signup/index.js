import React from "react";
import { Form, Input, Button, message } from "antd";
import { 
  postAuthor,
  postRemoteAuthor,
} from "../../requests/requestAuthor";
import { auth, remoteDomain, } from "../../requests/URL";

const layout = {
  labelCol: { span: 8 },
  wrapperCol: { span: 16 },
};

const tailLayout = {
  wrapperCol: { offset: 8, span: 16 },
};

export default class Signup extends React.Component {
  _isMounted = false;

  onFinish = (values) => {
    postAuthor(values).then((response) => {
      if (response.status === 200) {
        if (Object.keys(response.data).length === 1) {
          message.error("Registration failed: " + response.data.msg);
        } else {
          message.success("Registration successful: " + response.data.msg);
          // window.location.reload();
        }
      } else {
        message.error("Registration failed: " + response.data.msg);
      }
    });
    let params = {
      displayName: values.displayName,
      github: values.github,
      username: values.username,
      email: values.email,
      password: values.password,
      URL: `${remoteDomain}/author/`,
      auth: auth,
    };
    postRemoteAuthor(params).then((response) => {
      if (response.status === 200) {
        if (Object.keys(response.data).length === 1) {
          message.error("Remote Registration failed: " + response.data.msg);
        } else {
          message.success("Remote Registration successful: " + response.data.msg);
          // window.location.reload();
        }
      } else {
        message.error("Remote Registration failed: " + response.data.msg);
      }
    });
  };

  passwordValidator = async (rule, value) => {
    const passwordPattern = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/;
    if (!passwordPattern.test(value)) {
      return Promise.reject(
        new Error(
          "Please input your password at least 8 characters long, contains charaters and digits, without special characters."
        )
      );
    }
    return Promise.resolve();
  };

  render() {
    return (
      <div>
        <Form
          {...layout}
          name="register"
          initialValues={{ remember: true }}
          onFinish={this.onFinish}
        >
          <Form.Item
            label="Username"
            name="username"
            rules={[{ required: true, message: "Please input your username!" }]}
          >
            <Input />
          </Form.Item>

          <Form.Item
            label="Display Name"
            name="displayName"
            rules={[
              {
                required: true,
                message: "Please input your display name!",
              },
            ]}
          >
            <Input />
          </Form.Item>

          <Form.Item
            label="Password"
            name="password"
            rules={[
              {
                validator: this.passwordValidator,
              },
              { required: true, message: "Please input your password!" },
            ]}
          >
            <Input.Password />
          </Form.Item>

          <Form.Item
            label="Email"
            name="email"
            rules={[
              {
                type: "email",
                message: "The input is not valid E-mail!",
              },
              {
                required: true,
                message: "Please input your email address!",
              },
            ]}
          >
            <Input />
          </Form.Item>

          <Form.Item
            label="Github"
            name="github"
            rules={[
              {
                type: "url",
                message: "The input is not valid url!",
              },
              // { required: false, message: "Please input your github link!" },
            ]}
          >
            <Input />
          </Form.Item>

          <Form.Item {...tailLayout}>
            <Button type="primary" htmlType="submit">
              Submit
            </Button>
          </Form.Item>
        </Form>
      </div>
    );
  }
}
