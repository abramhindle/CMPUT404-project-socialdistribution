import React, { Component } from 'react'
import 'antd/dist/antd.css';
import { List, Avatar, Button } from 'antd';

const data = [
    {
        Username: 'Username1',
    },
    {
        Username: 'Username2',
    },
    {
        Username: 'Username3',
    },
    {
        Username: 'Username4',
    },
    {
        Username: 'Username5',
    },
    {
        Username: 'Username6',
    },
    {
        Username: 'Username7',
    },
    {
        Username: 'Username8',
    },
    {
        Username: 'Username9',
    },
    {
        Username: 'Username10',
    },
    {
        Username: 'Username11',
    },

];
  
class SignUpRequestContent extends Component {
    render() {
        return (
            <div>
                <List
                    itemLayout="horizontal"
                    dataSource={data}
                    renderItem={item => (
                    <List.Item>
                        <List.Item.Meta
                            avatar={<Avatar size="large" icon="user" />}
                            title={<a href='https://www.google.com'>{item.Username}</a>}
                            description="abcdefg@gmail.com"
                        />
                        <Button type="danger" shape="round" size='small'>
                            <span>Remove</span>
                        </Button>
                    </List.Item>
                    )}
                />
            </div>
        )
    }
}

export default SignUpRequestContent
