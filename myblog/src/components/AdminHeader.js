import React from 'react'
import { Layout, Menu, Icon, Button, Input, AutoComplete } from 'antd';
import 'antd/dist/antd.css';
import './AdminHeader.css'

const { Header } = Layout;
const { Search } = Input;

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
                        <Icon type="home" />
                        <span>Home</span>
                    </Menu.Item>
                    
                    <Search className = "admin-search"
                        placeholder="Search"
                        size="large"
                        enterButton
                    >
                    </Search>

                    <Menu.Item style={{float: 'right'}}key="logout">
                        <a href="https://www.google.com">
                            <span>Logout</span>
                        </a>
                    </Menu.Item>

                    <Menu.Item style={{float: 'right'}} key="Setting">
                        <Icon type="setting" />
                        <span>Setting</span>
                    </Menu.Item>
                </Menu> 
            </Header>
        </div>
    )
}

export default AdminHeader
