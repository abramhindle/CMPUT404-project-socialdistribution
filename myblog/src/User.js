import React from 'react';
import 'antd/dist/antd.css';
import { List,Button, Avatar } from 'antd';
import SimpleReactLightbox from "simple-react-lightbox";
import { SRLWrapper } from "simple-react-lightbox"; 
import './components/Header.css'
import validateCookie from './utils/utils.js';
import AuthorHeader from './components/AuthorHeader';
import axios from 'axios';
import cookie from 'react-cookies';
import './UserSelf.css';
import {reactLocalStorage} from 'reactjs-localstorage';

var urlpostid = '';
var urlauthorid = '';
var urljoin;
var commentUrl='';
var profileUrl='';

class User extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      size: 'large',
      PublicPostData:[],
      authorid:'',
      isloading : true
    }
  }

  componentDidMount() {
    validateCookie();
    this.fetchData();
  };

  fetchData = () => {
    axios.get('http://localhost:8000/api/post/', { headers: { 'Authorization': 'Token ' + cookie.load('token') } })
      .then(res => this.setState({
            PublicPostData : res.data,
            authorid: res.data[0].author,
            isloading:false 
          })
      ).catch(function (error) {
        console.log(error);
      });
  }

  handleAuthorClick = (author) => {
    urlauthorid = reactLocalStorage.set("urlauthorid", author);
    urljoin = require('url-join');
    profileUrl = urljoin("/author", urlauthorid);
    document.location.replace(profileUrl);
  }

  handleComment = (postId) => {
    reactLocalStorage.set("postid", postId);
    urlpostid = reactLocalStorage.set("urlpostid", postId);
    urljoin = require('url-join');
    commentUrl = urljoin("/posts", urlpostid, "/comments");
    document.location.replace(commentUrl);
  }
  
  render() {  
      return(!this.state.isloading ? 
        <view>
          <AuthorHeader/>
          <div className="mystyle">
              <List
                  itemLayout="vertical"
                  size="large"
                  pagination={{pageSize: 5 , hideOnSinglePage:true}}
                  dataSource={this.state.PublicPostData}
                  renderItem={item => (
                      <List.Item
                          key={item.title}
                          actions={[
                            <span>
                              <Button onClick={this.handleComment.bind(this, item.id)} icon="message" style={{width: "28px", height: "28px", backgroundColor: "white"}}></Button>
                              {0}
                            </span>
                          ]}
                          extra={
                            <SimpleReactLightbox>
                                <SRLWrapper>
                                  <img
                                    width={250}
                                    alt=""
                                    src="https://wallpaperaccess.com/full/628286.jpg"/>
                                  <img
                                  width={250}
                                  alt=""
                                  src="https://i.pinimg.com/originals/1f/53/25/1f53250c9035c9d657971712f6b38a99.jpg"/> 

                                </SRLWrapper> 
                            </SimpleReactLightbox>
                          }
                      >
                      <List.Item.Meta
                        avatar={<Avatar src={'https://cdn2.iconfinder.com/data/icons/user-icon-2-1/100/user_5-15-512.png'} />}
                        title={<a onClick={this.handleAuthorClick.bind(this, item.author)} href="#!">{item.author}</a>}
                      />
                      {item.published}<br/><br/>
                      {item.content}
                      </List.Item>
                  )}
              />
          </div>

        </view> : null
      );
    }
}


export default User;
