import React from 'react';

import { Form, Input, Button, Checkbox } from 'antd';
import { UserOutlined, LockOutlined, GithubOutlined } from '@ant-design/icons';

const RegisterForm = (props) => {
    const onFinish = (values) => {
        props.RegisterHandler(values); 
    };

    return (
    <Form
      name="normal_login"
      className="login-form"
      initialValues={{ remember: true }}
      onFinish={onFinish}
    >
          <Form.Item
            name="username"
            rules={[{ required: true, message: 'Please input your Username!' }]}
          >
            <Input prefix={<UserOutlined className="site-form-item-icon" />} placeholder="Username" />
          </Form.Item>
          <Form.Item
            name="github_url"
            rules={[{ required: true, message: 'Please input your Github URL!' }]}
          >
            <Input prefix={<GithubOutlined />} placeholder="Github URL" />
          </Form.Item>

          <Form.Item
            name="password"
            rules={[{ required: true, message: 'Please input your Password!' }]}
          >
            <Input
              prefix={<LockOutlined className="site-form-item-icon" />}
              type="password"
              placeholder="Password"
            />
          </Form.Item>

          <Form.Item>
            <Button type="primary" htmlType="submit" className="lgin-form-button">
             Register 
            </Button>
          </Form.Item>
        </Form>
    );
}

export default RegisterForm;
