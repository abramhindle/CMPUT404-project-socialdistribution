import React, {Component} from "react";
import {Form, Button} from 'semantic-ui-react';

export default class LoginComponent extends Component {

    constructor(props) {
        super(props)
        this.state = {
            usernameField: "",
            passwordField: ""
        }
    }

    sendLoginRequest = () => {
        let headers = {"Content-Type": "application/json"};
        let body = JSON.stringify({username: "test1", password: "test1" });
        const postRequest = fetch("/api/auth/login/", 
            { headers, method: "POST", body}).then((results) => {console.log(results, "oof")});
        return postRequest
    }
    render() {
        return(
            <div className="loginContainer">
                <Form>
                    <Form.Field>
                        <label>Username</label>
                        <input placeholder='Enter username' />
                    </Form.Field>
                    <Form.Field>
                        <label>Password</label>
                        <input type='password'/>
                    </Form.Field>
                    <Button type='submit' onClick={this.sendLoginRequest}>Submit</Button>
                </Form>
            </div>
        );
    }
}