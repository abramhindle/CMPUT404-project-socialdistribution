import { Form, Icon, Input, Button, Checkbox } from 'antd';
import React from "react";
import "antd/dist/antd.css";
// import {Checkbox} from "antd";
import "./components/Login.css"

class NormalLoginForm extends React.Component {
  handleSubmit = e => {
    e.preventDefault();
    this.props.form.validateFields((err, values) => {
      if (!err  &&
        (values.username === "admin" && values.password === "123")) {
        // console.log('Received values of form: ', values);
        console.log("Recived!");
      }else{alert("The combination of username and password is incorrect!")  
    }
    });
  };


  render() {
    const { getFieldDecorator } = this.props.form;
    return (
      <Form onSubmit={this.handleSubmit} className="login-form">
        <Form.Item>
          {getFieldDecorator('username', {
            rules: [{ required: true, message: 'Please input your username!' }],
          })(
            <Input
              prefix={<Icon type="user" style={{ color: 'rgba(0,0,0,.25)' }} />}
              placeholder="Username"
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
        </Form.Item>
        <Form.Item>
          {getFieldDecorator('remember', {
            valuePropName: 'checked',
            initialValue: true,
          })(<Checkbox>Remember me</Checkbox>)}
          <a className="login-form-forgot" href="!#">
            Forgot password
          </a>
          <br/>
          
          <Button type="primary" htmlType="submit" className="login-form-button" >
            <a href="./sign-up-request">
              Log in
            </a>
          </Button>
          
         <a style={{ float: "right" }} href="./register">Register</a>
        </Form.Item>
      </Form>
    );
  }
}

const WrappedNormalLoginForm = Form.create({ name: 'normal_login' })(NormalLoginForm);

// ReactDOM.render(<WrappedNormalLoginForm />, mountNode);

export default WrappedNormalLoginForm;