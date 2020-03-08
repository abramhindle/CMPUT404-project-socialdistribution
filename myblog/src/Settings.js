import React from 'react';
import 'antd/dist/antd.css';
import './index.css';
import { Form, Input, Button, Icon } from 'antd';
import axios from 'axios';
import './components/Settings.css';
import './components/Header.css';
import AuthorHeader from './components/AuthorHeader';

class ProfileContent extends React.Component {
    constructor(props) {
        super(props)
    
        this.state = {
            userName: null,
            email: null,
            displayName: null,
            github: null,
            bio: null,
        }
    }

    componentDidMount() {
        axios.get('http://localhost:8000/api/user/author/current_user/', 
        { headers: { 'Authorization': 'Token ' + document.cookie } }).then(res => {
            var userInfo = res.data;
            this.setState({userName: userInfo.username});
            this.setState({email: userInfo.email});
            this.setState({displayName: userInfo.displayName});
            this.setState({github: userInfo.github});
            this.setState({bio: userInfo.bio});
            console.log(this.state.userName);
          });
      };
    
    // handleSubmit = e => {
    //   this.props.form.validateFieldsAndScroll((err, values) => {
    //     if (!err) {
    //         var { username } = this.state.name;
    //       axios.post('http://localhost:8000/api/user/author/' + username + '/',
    //         {
    //             "github": values.github,
    //             "displayName": values.displayName,
    //             "bio": values.bio,
    //         },{ headers: { 'Authorization': 'Token ' + document.cookie } }
    //         )
    //         .then(function (response) {
    //           console.log(response);
    //           document.location.replace("/author/authorid")
    //         })
    //         .catch(function (error) {
    //           console.log(error);
    //         });
    //     }
    //   });
    // };  

    render(){
        // const { getFieldDecorator } = this.props.form;
        // const layout = {
        //     labelCol: {
        //       span: 8,
        //     },
        //     wrapperCol: {
        //       span: 16,
        //     },
        //   };
        return(
            <div>
            <span className="tag">User Name: <span className="info">{this.state.userName}</span></span>
              {/* <AuthorHeader/>
              <div className={'postInput'} style={{display: 'flex',  justifyContent:'center'}}>
                <Form {...layout}>

                    <Form.Item label="Display Name">
                        {getFieldDecorator("displayName")(<Input defaultValue={this.state.displayName}/>)}
                    </Form.Item>
                    
                    <Form.Item label="GitHub">
                        {getFieldDecorator("github")(<Input defaultValue={this.state.github}/>)}
                    </Form.Item>

                    <Form.Item label="Bio">
                        {getFieldDecorator("postContent")(<Input.TextArea defaultValue={this.state.bio}/>)}
                    </Form.Item>
            
                    <Form.Item wrapperCol={{ ...layout.wrapperCol, offset: 8 }}>
                        <Button type="primary" htmlType="button" onClick={this.handleSubmit}>
                            Save
                        </Button>
                    </Form.Item>
                </Form>
              </div> */}
            </div>

        )

    }
}

const WrappedProfileContent = Form.create({ name: 'ProfileContent' })(ProfileContent)


export default WrappedProfileContent
