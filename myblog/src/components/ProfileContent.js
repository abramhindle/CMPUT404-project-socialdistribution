import React, { Component } from 'react'
import 'antd/dist/antd.css';
import { Input, Button } from 'antd';
import './ProfileContent.css'

class ProfileContent extends Component {
    render() {
        return (
            <div className="profile">
                <h1 className="personal-info-header">Your Information</h1>
                <h2 className="display-id">ID: sadfihifh23947yfhcinbf86294e</h2>
                <span className="fieldname-text">UserName:</span>
                <Input className="info-input" defaultValue="AdminUserName" size="large"/>
                <br/>
                <span className="fieldname-text">Email:</span>
                <Input className="info-input" defaultValue="123456789@gmail.com" size="large"/>

                <div className="profile-save-button">
                    <Button type="primary" shape="round" size='large'>
                        <span>Save</span>
                    </Button>
                </div>

            </div>
        )
    }
}

export default ProfileContent
