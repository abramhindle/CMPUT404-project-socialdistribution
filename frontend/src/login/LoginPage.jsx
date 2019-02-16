import React, {Component} from "react";
import {Form, Button} from 'semantic-ui-react';
import {connect} from 'react-redux';
import store from "../store/index";

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

    /**
     * Used for login purposes. Used redux so that if components have no
     * direct child and parent relationship. The reasoning for this is that we need
     * a global store to be able to easier access whether we have logged in or not as well
     * as being able to easily access username and password for sending basic http requests for
     * authentication
     */
    sendLoginRequest = () => {
        console.log(this.props, "hello");
        const requireAuth = false,
            urlPath = "/api/auth/login/",
            requestBody = {username: this.state.usernameField,
                        password: this.state.passwordField};
        this.props.sendLogin(urlPath, requireAuth, requestBody);
    }

    /**
     * Example of how to do async GET request in the component
     * Should usually be done in componentDidMount
     */
    // sendGetRequest = (event) => {
    //     const requireAuth = true,
    //         urlPath = "/post/"
    //     HTTPFetchUtil.getRequest(urlPath, requireAuth)
    //         .then((httpResponse) => {
    //             if(httpResponse.status === 200) {
    //                 httpResponse.json().then((results) => {
    //                     console.log(results, "get results");
    //                 })
    //             }
    //         })
    //         .catch((error) => {
    //             console.error(error);
    //         });
    // }

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
                {/* {this.props.isValidated && <} */}
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
                    {/* <Button type='submit' onClick={this.sendGetRequest}> Test Get</Button> */}
                </Form>
            </div>
        );
    }
}

const mapStateToProps = state => {
    return {
        isValidated: state.isLoggedIn
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