import React, { Component } from 'react'
import 'antd/dist/antd.css';
import { Layout, Menu, Icon } from 'antd';

const { Sider } = Layout;

class AdminSideBar extends Component {

    render() {
        const {defaultSelectedKeys} = this.props
        return (
            <div>
                <Sider width={200} style={{ background: '#fff' }}>
                    <Menu
                        mode="inline"
                        defaultSelectedKeys={defaultSelectedKeys}
                        style={{ height: '100%', borderRight: 0 }}
                    >
                        <Menu.Item key="SignUpRequest">
                            <a href='/sign-up-request'>
                                <Icon type="bell"/>
                                <span>Sign Up Requests</span>
                            </a>
                        </Menu.Item>

                        <Menu.Item key="NodesRequest">
                            <a href='/nodes-request'>
                                <Icon type="plus-square"/>
                                <span>Nodes Requests</span>
                            </a>
                        </Menu.Item>

                        <Menu.Item key="MyNodes">
                            <a href='/my-nodes'>
                                <Icon type="bulb"/>
                                <span>My Nodes</span>
                            </a>
                        </Menu.Item>

                        <Menu.Item key="Authors">
                            <a href='/authors'>
                                <Icon type="team"/>
                                <span>My Authors</span>
                            </a>
                        </Menu.Item>

                    </Menu>
                </Sider>
            </div>
        )
    }
}

export default AdminSideBar