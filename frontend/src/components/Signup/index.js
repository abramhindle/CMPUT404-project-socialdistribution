import React from "react";
import { Form, Input, Button, message } from "antd";
import { postAuthor } from "../../requests/requestAuthor";

const layout = {
  labelCol: { span: 8 },
  wrapperCol: { span: 16 },
};

const tailLayout = {
  wrapperCol: { offset: 8, span: 16 },
};

export default class Signup extends React.Component {
  _isMounted = false;
  state = { authorID: "" };

  onFinish = (values) => {
    postAuthor(values).then((reponse) => {
      if (reponse.status === 200) {
        const uuidPattern = /(\w)+/g;
        const authorID = reponse.data.id;
        const matchList = authorID.match(uuidPattern);
        window.location.href = "/author/" + matchList[matchList.length - 1];
      } else {
        message.info("Registration fails.");
      }
    });
  };

  onFinishFailed = (errorInfo) => {
    message.error(errorInfo);
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
      <div
        style={{
          width: "300px",
          marginTop: "36px",
        }}
      >
        <Form
          {...layout}
          name="register"
          initialValues={{ remember: true }}
          onFinish={this.onFinish}
          onFinishFailed={this.onFinishFailed}
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
              { required: true, message: "Please input your github link!" },
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
