import React, { Component } from 'react'
import 'antd/dist/antd.css';
import { List, Button, Switch } from 'antd';

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
                        <Switch style={{marginRight: '30px'}} checkedChildren="Sharing Post" unCheckedChildren="Share Post"/>
                        <Switch style={{marginRight: '30px'}} checkedChildren="Sharing Image" unCheckedChildren="Share Image"/>
                        <Button type="danger" shape="round" size='small'>
                            Remove
                        </Button>
                    </List.Item>
                    )}
                />
            </div>
        )
    }
}

export default SignUpRequestContent
