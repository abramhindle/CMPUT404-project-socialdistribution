import React from 'react';
import 'antd/dist/antd.css';
import { List, Menu, Icon, Layout } from 'antd';
import { Button} from 'antd';
import { Input, Modal, Avatar } from 'antd';
import SimpleReactLightbox from "simple-react-lightbox";
import { SRLWrapper } from "simple-react-lightbox"; 
import axios from 'axios';


const { Header } = Layout;
const { confirm } = Modal;

function showDeleteConfirm() {
  confirm({
    title: 'Are you sure you want to delete this post?',
    okText: 'Yes',
    okType: 'danger',
    cancelText: 'No',
    onOk() {
      console.log('OK');
    },
    onCancel() {
      console.log('Cancel');
    },
  });
}


const IconText = ({ type, text }) => (
  <span>
    <Button href="/posts/postid/comments" color="OldLace" icon="message" style={{width: "28px", height: "28px", backgroundColor: "white"}}></Button>
    {text}
    <Button href="/postinput" color="OldLace" icon="edit" style={{left: "30%", width: "28px", height: "28px", backgroundColor: "white"}}></Button>
    <Button onClick={showDeleteConfirm} color="OldLace" icon="delete" style={{left: "50%", width: "28px", height: "28px", backgroundColor: "white"}}></Button>
  </span>
);


class UserSelf extends React.Component {
  state = {
    size: 'large',
    MyPostData:[],
    displayedName: "Name",
  };

  componentDidMount() {
    axios.get('http://localhost:8000/api/post/myPosts/', { headers: { 'Authorization': 'Token 99e4f57c63954dbdcf386f1b781a88c63df06175' } })

      .then(res => {
        const MyPost = res.data;
        this.setState({MyPostData: MyPost});
        if (MyPost.displayName === ''){
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
    const mystyle = {
      backgroundColor: "white",
      padding: "15px",
      color: "white",
      position: "relative",

    };

    const { Search } = Input;

      return(
        <view>
            <Header className="header">
                <Menu
                    theme="dark"
                    mode="horizontal"
                    style={{ lineHeight: '64px' }}
                >
                    <Menu.Item key="Home" >
                        <a href="/author/posts">
                            <Icon type="home" />
                            <span>Home</span>
                        </a>
                    </Menu.Item>
                    
                    <Search className="admin-search"
                        placeholder="Search"
                        size="large"
                        enterButton
                    >
                    </Search>

                    <Menu.Item style={{float: 'right'}} key="Logout">
                        <a href="/">
                            <span>Logout</span>
                        </a>
                    </Menu.Item>

                    <Menu.Item style={{float: 'right'}} key="Settings">
                        <a href="/Settings">
                            <span>Settings</span>
                        </a>
                    </Menu.Item>

                    <Menu.Item style={{float: 'right'}} key="Friends">
                        <a href="/author/friends">
                            <span>Friends</span>
                        </a>
                    </Menu.Item>

                    <Menu.Item style={{float: 'right'}} key="Postinput">
                        <a href="/postinput">
                            <span>What's on your mind</span>
                        </a>
                    </Menu.Item>

                </Menu> 
            </Header>

          <div style={mystyle}>
              <List
                  itemLayout="vertical"
                  size="large"
                  pagination={{pageSize: 5}}
                  dataSource={this.state.MyPostData}
                  renderItem={item => (
                      <List.Item
                          key={item.title}
                          actions={[
                          <IconText type="message" text="0" key="list-vertical-message" />,
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
