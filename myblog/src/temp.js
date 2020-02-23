import React from 'react';
// import ReactDOM from 'react-dom';
import 'antd/dist/antd.css';
import './index.css';
import "./CSS/register.css"

import {
  Form,
  Input,
  Tooltip,
  Icon,
  Button,
  Select,
  Checkbox,
  DatePicker,
} from 'antd';

// const { Option } = Select;
class RegistrationForm extends React.Component {
  state = {
    confirmDirty: false,
    autoCompleteResult: [],
  };

  handleSubmit = e => {
    e.preventDefault();
    this.props.form.validateFieldsAndScroll((err, values) => {
      if (!err) {
        console.log('Received values of form: ', values);
      }
    });
  };

  handleConfirmBlur = e => {
    const { value } = e.target;
    this.setState({ confirmDirty: this.state.confirmDirty || !!value });
  };

  compareToFirstPassword = (rule, value, callback) => {
    const { form } = this.props;
    if (value && value !== form.getFieldValue('password')) {
      callback('Two passwords that you enter is inconsistent!');
    } else {
      callback();
    }
  };

  validateToNextPassword = (rule, value, callback) => {
    const { form } = this.props;
    if (value && this.state.confirmDirty) {
      form.validateFields(['confirm'], { force: true });
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
            sm: { span: 8 },
        },
        wrapperCol: {
            xs: { span: 24 },
            sm: { span: 8 },
        },
        };
        const tailFormItemLayout = {
        wrapperCol: {
            xs: {
            span: 24,
            offset: 0,
            },
            sm: {
            span: 16,
            offset: 18,
            },
          },
        };
        
    return (

      <Form {...formItemLayout} onSubmit={this.handleSubmit}>
        <Form.Item label="E-mail">
          {getFieldDecorator('email', {
            rules: [
              {
                type: 'email',
                message: 'The input is not valid E-mail!',
              },
              {
                required: true,
                message: 'Please input your E-mail!',
              },
            ],
          })(<Input />)}
        </Form.Item>
        
        <Form.Item label="Password" hasFeedback>
          {getFieldDecorator('password', {
            rules: [
              {
                required: true,
                message: 'Please input your password!',
              },
              {
                validator: this.validateToNextPassword,
              },
            ],
          })(<Input.Password />)}
        </Form.Item>

        <Form.Item label="Confirm Password" hasFeedback>
          {getFieldDecorator('confirm', {
            rules: [
              {
                required: true,
                message: 'Please confirm your password!',
              },
              {
                validator: this.validateGender,
              },
            ],
          })(<Input.Password onBlur={this.handleConfirmBlur} />)}
        </Form.Item>

        <Form.Item
          label={
            <span>
              Nickname&nbsp;
              <Tooltip title="What do you want others to call you?">
                <Icon type="question-circle-o" />
              </Tooltip>
            </span>
          }
        >
          {getFieldDecorator('nickname', {
            rules: [{ required: true, message: 'Please input your nickname!', whitespace: true }],
          })(<Input />)}
        </Form.Item>
        
{/* 
        <Form.Item label="Birthday">
          {getFieldDecorator('birthday',{
              rules: [
                {
                  required: true,
                  type: 'date',
                  message: 'what is your birthday?',
                }, {
                  validator: this.checkBirthday,
                }],
            })(           
          <DatePicker/>,
        )}
        </Form.Item> */}


        {/* <Form.Item label="Gender">
          {getFieldDecorator('gender', {
            rules: [{ required: false, message: 'Please select your gender!' }],
          })(
            <Select
              onChange={this.handleSelectChange}
            >
              <Option value="male">male</Option>
              <Option value="female">female</Option>
            </Select>,
          )}
        </Form.Item> */}


        <Form.Item {...tailFormItemLayout}>
                  {getFieldDecorator("agreement", {
                    valuePropName: "checked"
                  })(
                    <Checkbox>
                      I have read the <a href="">agreement</a>
                    </Checkbox>
                  )}
                </Form.Item>



        <Form.Item {...tailFormItemLayout}>
          <Button type="primary" htmlType="submit">
            Register
          </Button>
        </Form.Item>
      </Form>
    ); 
    }
}

const WrappedRegistrationForm = Form.create({ name: 'register' })(RegistrationForm);

// ReactDOM.render(<WrappedRegistrationForm />, document.getElementById('container'));
export default WrappedRegistrationForm;