import React, {Component} from "react";
import {Form, Button} from 'semantic-ui-react';
import {Route, Redirect} from "react-router-dom";
import HTTPFetchUtil from "../util/HTTPFetchUtil";
import {connect} from 'react-redux';

import * as LoginActions from "../actions/LoginActions";

class LoginComponent extends Component {

    constructor(props) {
        super(props)
        this.state = {
            usernameField: "",
            passwordField: "",
            isLoggedIn: false
        }
    }

    sendLoginRequest = (event) => {
        const requireAuth = true,
            urlPath = "/api/auth/login/",
            requestBody = {username: this.state.usernameField,
                        password: this.state.passwordField};
        this.props.sendLogin(urlPath, false, requestBody);
    }

    onUsernameInput = (event, usernameInput) => {
        this.setState({
            usernameField: usernameInput.value
        });
    }

    onPasswordInput = (event, passwordInput) => {
        this.setState({
            passwordField: passwordInput.value
        })
    }

    render() {
        return(
            <div className="loginContainer">
                <Form>
                    <Form.Input
                        onChange={this.onUsernameInput}>
                        <label>Username</label>
                        <input placeholder='Enter username' />
                    </Form.Input>
                    <Form.Input
                         onChange={this.onPasswordInput}>
                        <label>Password</label>
                        <input type='password'/>
                    </Form.Input>
                    <Button type='submit' onClick={this.sendLoginRequest}>Submit</Button>
                </Form>
            </div>
        );
    }
}

const mapStateToProps = state => {
    return {
        state: state.isLoggedIn
    }
}

const mapDispatchToProps = dispatch => {
    return {
        sendLogin: (urlPath, requireAuth, requestBody) => {
            return dispatch(LoginActions.sendLogin(urlPath, requireAuth, requestBody));
        }
    }
}


export default connect(mapStateToProps, mapDispatchToProps)(LoginComponent); // connecting to the store causes the re-render