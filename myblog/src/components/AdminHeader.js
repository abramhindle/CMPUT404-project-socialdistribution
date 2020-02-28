import React from 'react'
import { Layout, Menu, Icon, Input } from 'antd';
import 'antd/dist/antd.css';
import './AdminHeader.css'

const { Header } = Layout;
const { Search } = Input;
const { SubMenu } = Menu;

function AdminHeader() {
    return (
        <div>
            <Header className="header">
                <Menu
                    theme="dark"
                    mode="horizontal"
                    defaultSelectedKeys={['Home']}
                    style={{ lineHeight: '64px' }}
                >
                    <Menu.Item key="Home">
                        <a href="/">
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

                    <SubMenu 
                        style={{float: 'right'}}
                        key="Setting"
                        title={
                        <span>
                            <Icon type="setting"/>
                            <span>Setting</span>
                        </span>
                        }
                    >
                        <Menu.Item key="Profile">
                            <a href='/profile'>
                                <Icon type="user"/>
                                <span>My Profile</span>
                            </a>
                        </Menu.Item>
                        <Menu.Item key="AddNodes">
                            <a href='/add-nodes'>
                                <Icon type="plus-circle"/>
                                <span>Add Nodes</span>
                            </a>
                        </Menu.Item>
                    </SubMenu>
                </Menu> 
            </Header>
        </div>
    )
}

export default AdminHeader
