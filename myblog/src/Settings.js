import React, { Component } from 'react'
import 'antd/dist/antd.css';
import { Input, Button } from 'antd';
import './components/Settings.css'

class ProfileContent extends Component {
    render() {
        return (
            <div className="profile">
                <h1 className="info-header">Your Profile</h1>
                <h2 className="display-id">Username</h2>

                <span className="fieldname-text">First Name:</span>
                <Input className="info-input" defaultValue="" size="large"/>
                <br/>

                <span className="fieldname-text">Last Name:</span>
                <Input className="info-input" defaultValue="" size="large"/>
                <br/>

                <span className="fieldname-text">Github:</span>
                <Input className="info-input" defaultValue="" size="large"/>
                <br/>

                <span className="fieldname-text">Bio:</span>
                <Input className="info-input" defaultValue="" size="large"/>

                <div className="profile-save-button">
                    <Button type="primary" shape="round" size='large' href="/author/authorid">
                        <span>Update My Profile</span>
                    </Button>
                </div>

            </div>
        )
    }
}

export default ProfileContent
