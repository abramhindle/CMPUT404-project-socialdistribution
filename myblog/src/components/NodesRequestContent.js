import React, { Component } from 'react'
import 'antd/dist/antd.css';
import { List, Avatar, Button, Switch, Layout } from 'antd';

const data = [
    {
        ServerName: 'ServerName1',
    },
    {
        ServerName: 'ServerName2',
    },
    {
        ServerName: 'ServerName3',
    },
];
  

export class SignUpRequestContent extends Component {
    render() {
        return (
            <div>
                <List
                    itemLayout="horizontal"
                    size = "large"
                    dataSource={data}
                    renderItem={item => (
                    <List.Item>
                        <List.Item.Meta
                            title={<a>{item.ServerName}</a>}
                            description="Host: localhost, Port: 8080"
                        />
                        <Button type="primary" style={{marginRight: '60px'}} shape="round" size='small'>
                            Connect
                        </Button>
                    </List.Item>
                    )}
                />
            </div>
        )
    }
}

export default SignUpRequestContent
