import React from 'react'
import { Layout, Menu, Icon, Input } from 'antd';
import 'antd/dist/antd.css';
import './Header.css';
import cookie from 'react-cookies';

const { Header } = Layout;
const { Search } = Input;
const { SubMenu } = Menu;

class AuthorHeader extends React.Component {

    logout = () => {
        cookie.remove('token', { path: '/' })
        document.location.replace("/")
    }

    render() {
        return (
            <div>
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
                        
                        <Search className="search"
                            placeholder="Search Friends"
                            size="large"
                            enterButton
                        >
                        </Search>

                        <Menu.Item style={{float: 'right'}} key="Logout">
                            <a href="#!" onClick={this.logout}>
                                <span>Logout</span>
                            </a>
                        </Menu.Item>

                        <SubMenu 
                            style={{float: 'right'}}
                            key="Friends"
                            title={
                            <span>
                                <span>Friends</span>
                            </span>
                            }
                        >
                            <Menu.Item key="Profile">
                                <a href='/author/friends'>
                                    <span>Friend List</span>
                                </a>
                            </Menu.Item>
                            <Menu.Item key="AddNodes">
                                <a href='/friendrequest'>
                                    <span>Friend Request</span>
                                </a>
                            </Menu.Item>
                        </SubMenu>

                        <Menu.Item style={{float: 'right'}} key="Postinput">
                            <a href="/postinput">
                                <span>What's on your mind</span>
                            </a>
                        </Menu.Item>

                        <Menu.Item style={{float: 'right'}} key="MyPost">
                            <a href="/author/authorid" >
                                <span>My Profile</span>
                            </a>
                        </Menu.Item>
                    </Menu> 
                </Header>
            </div>
        )
    }
}

export default AuthorHeader