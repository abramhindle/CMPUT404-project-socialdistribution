import { Form, Icon, Input, Button, Checkbox, message } from 'antd';
import React from "react";
import "antd/dist/antd.css";
import cookie from 'react-cookies'
import "./components/Login.css"
import axios from 'axios' ;
import {login_api} from "./utils/utils.js";

class NormalLoginForm extends React.Component {

  checkCookie = () => {

    if(cookie.load('token')){
      document.location.replace("/author/posts")
      return true;
    }else return false;
  }

  handleSubmit = e => {
    this.props.form.validateFields((err, values) => {
      if (!err){
        let config = {
          "Content-type":"application/json"
        }
        axios.post(login_api,
          {
            "email": values.Email,
            "password":values.password
          },config
          ).then(function (response) {
              cookie.save('token', response.data['key'], { path: '/' })
              document.location.replace("/author/posts")
          }).catch((error) => {
              let msg = JSON.parse(error.response.request.response);
              message.error(msg['non_field_errors'][0])
          });
      }
    })
  };

  render() {
    if (this.checkCookie()===true) return;
    const { getFieldDecorator } = this.props.form;
    return (
      <div> 
      <Form className="login-form">
        <Form.Item>
          {getFieldDecorator('Email', {
            rules: [
              { required: true, message: 'Please input your address!' },
              {
                type: "email",
                message: "The input is not valid E-mail!"
              }
            ]
          })(
            <Input
              prefix={<Icon type="user" style={{ color: 'rgba(0,0,0,.25)' }} />}
              placeholder="Email Address"
            />,
          )}
        </Form.Item>
        <Form.Item>
          {getFieldDecorator('password', {
            rules: [{ required: true, message: 'Please input your Password!' }],
          })(
            <Input
              prefix={<Icon type="lock" style={{ color: 'rgba(0,0,0,.25)' }} />}
              type="password"
              placeholder="Password"
            />,
          )}
          {getFieldDecorator('remember', {
            valuePropName: 'checked',
            initialValue: true,
          })(<Checkbox>Remember me</Checkbox>)}
        </Form.Item>
      </Form>
        <a className="login-to-register" href="./register">Register</a>
        <Button type="primary" htmlType="button" className="login-form-button" onClick={this.handleSubmit}>
            Log in
        </Button>
    </div>
    );
  }
}

const WrappedNormalLoginForm = Form.create({ name: 'normal_login' })(NormalLoginForm);
export default WrappedNormalLoginForm;