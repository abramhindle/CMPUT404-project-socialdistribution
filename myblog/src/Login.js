import { Form, Icon, Input, Button, Checkbox } from 'antd';
import React from "react";
import "antd/dist/antd.css";
// import {Checkbox} from "antd";
import "./components/Login.css"
import axios from 'axios' ;
const url ="http://127.0.0.1:8000/api/user/login/";

class NormalLoginForm extends React.Component {
  


  handleSubmit = e => {
    this.props.form.validateFields((err, values) => {
      console.log(values)
      // alert(values.Email)
      if (!err){
        let config = {
          "Content-type":"application/json"
        }
        axios.post(url,
          {
            "email": values.Email,
            "password":values.password
          },config
          )

          .then(function (response) {
            console.log(response);
            // this.status = response.json()
            document.location.replace("/author/posts")
          })

          .catch(function (error) {
            if (error.response) {
              let data = error.response.data;
              alert(data["non_field_errors"][0])
            }
          });
      }
    })
  };


  render() {
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

// ReactDOM.render(<WrappedNormalLoginForm />, mountNode);

export default WrappedNormalLoginForm;