import React, {Component} from "react";
import {Form, Button} from 'semantic-ui-react';
import {Route, Redirect} from "react-router-dom";
import HTTPFetchUtil from "../util/HTTPFetchUtil";

export default class LoginComponent extends Component {

    constructor(props) {
        super(props)
        this.state = {
            usernameField: "",
            passwordField: ""
        }
    }

    sendLoginRequest = () => {
        // let headers = {"Content-Type": "application/json", 'Authorization': 'Basic ' + window.btoa("test1" + ':' + "test1")};
        // let body = JSON.stringify({github: "derricks numbani github"});
        // return fetch("/api/profile/", {headers, body, method: "POST"})
        // return fetch("/api/post/", {headers, })
        //     .then((res) => {
        //         console.log(res, "kevin chang")
        //     });
        // const body = {github: "derricks numbani github"},
        //     requireAuth = true,
        //     endpointURL = "/api/profile/";
        // console.log("nani teh fuck 1")
        HTTPFetchUtil.sendPostRequest()
            .then((result) => {
                console.log(result, "derrick's numbani")
            }).catch((err) => {
                console.error(err);
            });
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