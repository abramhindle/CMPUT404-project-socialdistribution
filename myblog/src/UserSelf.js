import React from 'react';
import 'antd/dist/antd.css';
import { List, Avatar, Menu, Icon, Layout } from 'antd';
import { Button} from 'antd';
import { Input, Modal } from 'antd';
import SimpleReactLightbox from "simple-react-lightbox";
import { SRLWrapper } from "simple-react-lightbox"; 
const { Header } = Layout;
const { confirm } = Modal;


const listData = [];
for (let i = 0; i < 50; i++) {
  listData.push({
    href: 'http://ant.design',
    title: `Me`,
    avatar: 'https://qph.fs.quoracdn.net/main-qimg-54166a525ee4fb3097d260173688c157.webp',
    description:
      '2020-02-02',
    content:
      'Icelandair is linking to the weather forecast for the northern lights show that day providing a nice educational tip for their fans.  But they take it a step further by asking people to share their photos.',
  });
}


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
                    <Menu.Item key="Home">
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
                  dataSource={listData}
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
                        avatar={<Avatar src={item.avatar} />}
                        title={<a href={item.href}>{item.title}</a>}
                        description={item.description}
                      />
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
