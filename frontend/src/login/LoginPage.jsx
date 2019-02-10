import React, {Component} from "react";
import {Form, Button} from 'semantic-ui-react';
import {Route, Redirect} from "react-router-dom";

export default class LoginComponent extends Component {

    constructor(props) {
        super(props)
        this.state = {
            usernameField: "",
            passwordField: ""
        }
    }

    sendLoginRequest = () => {
        // let headers = {"Content-Type": "application/json", 'Authorization': 'Basic' + window.btoa("test1" + ":" +"test1")};
        // // let body = JSON.stringify({username: "test1", password: "test1" });
        // let body = JSON.stringify({github: "derrick wai in numbani"});
        // // const request = fetch("/api/profile/", {headers, })
        // //     .then((request) => {
        // //         console.log(request, "first profile")
        // //     });
        // const postRequest = fetch("/api/profile/", 
        //     { headers, method: "POST", body}).then((results) => {
        //         console.log(results.headers.Headers, "adfda")
        //         if(results.status === 200) {
        //             console.log(this.props.history, "kevin chang")
        //             this.props.history.push("/stream");
        //         }
            
        //     });
        let headers = {"Content-Type": "application/json", 'Authorization': 'Basic ' + window.btoa("test1" + ':' + "test1")};
        let body = JSON.stringify({github: "derricks numbani github"});
        return fetch("/api/profile/", {headers, body, method: "POST"})
        //return fetch("/api/post/", {headers, })
            .then((res) => {
                console.log(res, "kevin chang")
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