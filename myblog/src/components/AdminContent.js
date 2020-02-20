import React, { Component } from 'react'
import 'antd/dist/antd.css';
import { List, Avatar, Button, Switch } from 'antd';

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
  

export class AdminContent extends Component {
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
                            title={<a>{item.Username}</a>}
                            description="abcdefg@gmail.com"
                        />
                        <Switch style={{marginRight: '30px'}} checkedChildren="Approved" unCheckedChildren="Approve"/>
                        <Button type="danger" shape="round" size='small'>
                            Delete
                        </Button>
                    </List.Item>
                    )}
                />,
            </div>
        )
    }
}

export default AdminContent
