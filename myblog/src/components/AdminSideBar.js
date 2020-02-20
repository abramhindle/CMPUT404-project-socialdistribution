import React, { Component } from 'react'
import 'antd/dist/antd.css';
import { Layout, Menu, Icon, Badge } from 'antd';

const { Sider } = Layout;


class AdminSideBar extends Component {

    render() {
        return (
            <div>
                <Sider width={200} style={{ background: '#fff' }}>
                    <Menu
                        mode="inline"
                        defaultSelectedKeys={['SignUpRequest']}
                        style={{ height: '100%', borderRight: 0 }}
                    >
                        <Menu.Item key="SignUpRequest">
                            <Icon type="bell"/>
                            <span>Sign Up Requests</span>
                        </Menu.Item>

                        <Menu.Item key="User">
                            <Icon type="user"/>
                            <span>My authors</span>
                        </Menu.Item>

                        <Menu.Item key="Nodes">
                            <Icon type="bulb"/>
                            <span>My Nodes</span>
                        </Menu.Item>
                    </Menu>
                </Sider>
            </div>
        )
    }
}

export default AdminSideBar
