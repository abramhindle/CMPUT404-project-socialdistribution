import React from 'react';
import 'antd/dist/antd.css';
import { List, Button, Modal, Avatar} from 'antd';
import SimpleReactLightbox from "simple-react-lightbox";
import { SRLWrapper } from "simple-react-lightbox"; 
import axios from 'axios';
// import './components/Header.css'
// import './components/AuthorProfile.css'
import AuthorHeader from './components/AuthorHeader'
import AuthorProfile from './components/AuthorProfile'
import './UserSelf.css'

const { confirm } = Modal;

class UserSelf extends React.Component {
  state = {
    size: 'large',
    MyPostData:[],
    displayedName: "Name",
  };

  showDeleteConfirm = (postId) => {
    confirm({
      title: 'Are you sure you want to delete this post?',
      okText: 'Yes',
      okType: 'danger',
      cancelText: 'No',
      onOk() {
        console.log(postId);
        axios.delete('http://localhost:8000/api/post/myPosts/' + String(postId) + '/', { headers: { 'Authorization': 'Token ' + document.cookie } })
        .then(function () {
          document.location.replace("/author/authorid")
        })
      },
      onCancel() {
        console.log('Cancel');
      },
    });
  }

  componentDidMount() {
    axios.get('http://localhost:8000/api/post/myPosts/', { headers: { 'Authorization': 'Token ' + document.cookie } })
      .then(res => {
        const MyPost = res.data;
        this.setState({MyPostData: MyPost});
        if(MyPost.displayName === ''){
            this.setState({displayedName: MyPost.userName})
        }
        else{
            this.setState({displayedName: MyPost.displayName})
        }
        console.log(this.state.displayedName)    
      })
     
      .catch(function (error) {
      console.log(error);
      });
  };


  render() {

      return(
        <view>
          <AuthorHeader/>
          <div className="mystyle">
              <AuthorProfile/>
              <List
                  itemLayout="vertical"
                  size="large"
                  pagination={{pageSize: 5}}
                  dataSource={this.state.MyPostData}
                  renderItem={item => (
                      <List.Item
                          key={item.title}
                          actions={[
                          <span>
                            <Button href="/posts/postid/comments" color="OldLace" icon="message" style={{width: "28px", height: "28px", backgroundColor: "white"}}></Button>
                            {0}
                            <Button href="/postinput" color="OldLace" icon="edit" style={{left: "30%", width: "28px", height: "28px", backgroundColor: "white"}}></Button>
                            <Button onClick={this.showDeleteConfirm.bind(this, item.id)} color="OldLace" icon="delete" style={{left: "50%", width: "28px", height: "28px", backgroundColor: "white"}}></Button>
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
                        title={item.author.username}
                      />
                      {item.published}<br/><br/>
                      {item.content}                      
                      </List.Item>
                  )}
              />
          </div>
        </view>

      );
    }
}


export default UserSelf;
