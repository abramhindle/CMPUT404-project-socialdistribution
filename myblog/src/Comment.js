import React from 'react';
import 'antd/dist/antd.css';
import { Form, Comment, Avatar, List, Radio } from 'antd';
import { Input } from 'antd';
import { Button} from 'antd';
import {reactLocalStorage} from 'reactjs-localstorage';
import cookie from 'react-cookies';
import axios from 'axios';
import AuthorHeader from './components/AuthorHeader'
import {post_api}  from "./utils/utils.js";
const { TextArea } = Input;
var id = '';

class Comments extends React.Component {

  state = {
    commentInput:'',
    commentData:[],
  }

  componentDidMount() {
    id = reactLocalStorage.get("postid");
    axios.get(post_api + String(id) + '/get_comments/', { headers: { 'Authorization': 'Token ' + cookie.load('token')}})
    .then(res => {
      const getComment = res.data;
      this.setState({commentData: getComment});
      console.log(this.state.commentData);
    })
    .catch(function (error) {
    console.log(error);
    });

    //reactLocalStorage.clear();
};


    handleSubmit = e => {
      this.props.form.validateFieldsAndScroll((err, values) => {
        if (!err) {              
          axios.post(post_api + String(id) + '/post_comment/',
            {
              content: values.commentContent,  
              contentType: values.commentType,      
            },{ headers: { 'Authorization': 'Token ' + cookie.load('token') } }
            )
            .then(function (response) {
              console.log(response);
              window.location.reload(false);
              //document.location.replace("/posts/postid/comments")

            })
            .catch(function (error) {
              console.log(error);
            });
        }
      });
    };  

    render(){
      const { getFieldDecorator } = this.props.form;

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

        return(
          <view>
              <AuthorHeader/>
              <div className={'comment'} style={{justifyContent:'center', padding: '2%', width:'100%'}} >
              <Form >
                <Form.Item>
                    <List
                        className="comment-list"
                        header={`${this.state.commentData.length} comment(s)`}
                        itemLayout="horizontal"
                        dataSource={this.state.commentData}
                        renderItem={item => (
                            <li>
                                <Comment
                                    author={item.author}
                                    avatar={<Avatar src={'https://cdn2.iconfinder.com/data/icons/user-icon-2-1/100/user_5-15-512.png'} />}                                    
                                    content={item.content}
                                    datetime={item.published}
                                />
                            </li>
                        )}
                    />
                </Form.Item>

                <Form.Item>
                      {getFieldDecorator("commentContent", {
                        rules: [
                          {
                            required: false,
                            whitespace: true
                          }
                        ],
                      })(<TextArea rows={2} placeholder="Enter your comment here"/>)}
                    </Form.Item>


                <Form.Item>
                  {getFieldDecorator("commentType", {
                    rules: [
                      {
                        required: false,
                      },
                    ],
                  })(<Radio.Group>
                        <Radio.Button value="text/plain">Plain Text</Radio.Button>
                        <Radio.Button value="text/markdown">Markdown</Radio.Button>
                      </Radio.Group>
                  )}
                </Form.Item>
        
                <Form.Item {...tailFormItemLayout}>
                  <Button type="primary" htmlType="button" onClick={this.handleSubmit}>
                        Comment
                  </Button>
                </Form.Item>
              </Form>
            </div>
        </view>    

        )


    }

}


const WrappedComments = Form.create({ name: 'Comment' })(Comments)

export default WrappedComments;

