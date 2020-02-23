import React, { Component } from 'react'
import 'antd/dist/antd.css';
import { List, Button } from 'antd';

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
  

class SignUpRequestContent extends Component {
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
                            title={<a href="!#">{item.ServerName}</a>}
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
