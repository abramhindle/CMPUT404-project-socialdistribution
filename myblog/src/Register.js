import React from "react";
// import ReactDOM from "react-dom";
import "antd/dist/antd.css";
import './components/Register.css';
import { Form, Input, Tooltip, Icon, Button, Checkbox } from 'antd';
import axios from 'axios' ;

// const { Header, Footer, Sider, Content } = Layout;

class RegistrationForm extends React.Component {
  state = {
    confirmDirty: false,
    autoCompleteResult: []
  };

  test = e =>{
    e.preventDefault();
    alert("111111")
    console.log("Received values of form: ");
  //   let config = {
  //   "Content-type":"application/json"
  // }

    let  url = "http://localhost:8000/api/user/signup/"
    axios.post(url,
      {
        "username":"user3",
        "email":"user1232@gmail.com",
        "password1":"passqwer",
        "password2":"passqwer"
      }
      
      )

      .then(function (response) {
        console.log(response);
      })
      .catch(function (error) {
        console.log(error);
      });
  }

  handleSubmit = e => {
    e.preventDefault();
    this.props.form.validateFieldsAndScroll((err, values) => {
      if (!err) {
        alert("111111")
        console.log("Received values of form: ", values);
        let config = {
        "Content-type":"application/json"
      }

        let  url = "http://localhost:8000/api/user/signup/"
        axios.post(url,
          {
            "username":"user2",
            "email":"user2@gmail.com",
            "password1":"passqwer",
            "password2":"passqwer"
          },config
          
          )

          .then(function (response) {
            console.log(response);
          })
          .catch(function (error) {
            console.log(error);
          });
      }
    });
  };

  handleConfirmBlur = e => {
    const { value } = e.target;
    this.setState({ confirmDirty: this.state.confirmDirty || !!value });
  };

  compareToFirstPassword = (rule, value, callback) => {
    const { form } = this.props;
    if (value && value !== form.getFieldValue("password")) {
      callback("Two passwords that you enter is inconsistent!");
    } else {
      callback();
    }
  };

  validateToNextPassword = (rule,value, callback) => {
    const { form } = this.props;
    if (value && this.state.confirmDirty) {
      form.validateFields(["confirm"], { force: true });
    }
    callback();
  };

    // handleSelectChange = value => {
  //   console.log(value);
  //   this.props.form.setFieldsValue({
  //       });
  // };

  // checkBirthday(value, callback) {
  //   if (value && value.getTime() >= Date.now()) {
  //     callback('The day beyond today');
  //   } else {
  //     callback();
  //   }
  // };

  render() {

    const { getFieldDecorator } = this.props.form;

    const formItemLayout = {
      labelCol: {
        xs: { span: 24 },
        sm: { span: 8 }
      },
      wrapperCol: {
        xs: { span: 24 },
        sm: { span: 8 }
      }
    };
    const tailFormItemLayout = {
      wrapperCol: {
        xs: {
          span: 24,
          offset: 0
        },
        sm: {
          span: 16,
          offset: 8
        }
      }
    };

    return (
      <div className = 'register'>
      <Form {...formItemLayout} onSubmit={this.handleSubmit}>
        
      <Form.Item
          label={
            <span>
              Username&nbsp;
            </span>
          }
        >
          {getFieldDecorator("username", {
            rules: [
              {
                required: true,
                message: "Please input your username!",
                whitespace: true
              }
            ]
          })(<Input />)}
        </Form.Item>
        
        <Form.Item label="E-mail">
          {getFieldDecorator("email", {
            rules: [
              {
                type: "email",
                message: "The input is not valid E-mail!"
              },
              {
                required: true,
                message: "Please input your E-mail!"
              }
            ]
          })(<Input />)}
        </Form.Item>

        <Form.Item label="Password" hasFeedback>
          {getFieldDecorator("password", {
            rules: [
              {
                required: true,
                message: "Please input your password!"
              },
              {
                validator: this.validateToNextPassword
              }
            ]
          })(<Input.Password />)}
        </Form.Item>
        <Form.Item label="Confirm Password" hasFeedback>
          {getFieldDecorator("confirm", {
            rules: [
              {
                required: true,
                message: "Please confirm your password!"
              },
              {
                validator: this.compareToFirstPassword
              }
            ]
          })(<Input.Password onBlur={this.handleConfirmBlur} />)}
        </Form.Item>

        <Form.Item {...tailFormItemLayout}>
          {getFieldDecorator("agreement", {
            valuePropName: "checked"
          })(
            <Checkbox>
              I have read the <a href="!#">agreement</a>
            </Checkbox>
          )}
        </Form.Item>
        <Form.Item {...tailFormItemLayout}>
          <Button type="primary" htmlType="submit" onClick={this.test}>
            <a href="">
                Register
            </a>
          </Button>
        </Form.Item>
      </Form>
    </div>
    );
  }
}

const WrappedRegistrationForm = Form.create({ name: 'register' })(RegistrationForm)
// ReactDOM.render(<WrappedRegistrationForm />, document.getElementById('container'));
export default WrappedRegistrationForm;