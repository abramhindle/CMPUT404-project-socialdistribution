import React, { Component } from 'react'
import 'antd/dist/antd.css';
import { Input, Col, Row, Button } from 'antd';
import './AddNodesContent.css'

const InputGroup = Input.Group;

class AddNodesContent extends Component {
    render() {
        return (
            <div>
                <h1 className="add-nodes-header">Enter the information of the node you want to add:</h1>
                <span className="add-nodes-hint">Server Name: </span>
                <Input className="server-name-input" size="large"/>
                <InputGroup className="host-port" size="large">
                    <Row gutter={50}>
                        <Col span={10}>
                            <Input placeholder="Host" />
                        </Col>
                        <Col span={8}>
                            <Input placeholder="Post Number" />
                        </Col>
                    </Row>
                </InputGroup>
                <div className="add-Nodes-button">
                    <Button type="primary" shape="round" size='large'>
                        <span>Add</span>
                    </Button>
                </div>

            </div>
        )
    }
}

export default AddNodesContent
