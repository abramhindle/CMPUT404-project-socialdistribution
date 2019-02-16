import React, { Component } from 'react';
import { Input } from 'semantic-ui-react'
import {connect} from 'react-redux';
import * as LoginActions from "../actions/LoginActions";
import { Redirect, BrowserRouter} from "react-router-dom";
import store from "../store/index";
import Async from 'react-promise'

class LoginFormComponent extends Component {	

	constructor(props) {
		super(props);
		this.state = {
            username: "",
            password: "",
            isLoggedIn: false,
		}
	}	

    handleRegisterClick = () => {
        this.props.changePage();
    }

    attemptLogin = (props) => {
        const requireAuth = false,
            urlPath = "/api/auth/login/",
            requestBody = {username: this.state.username,
                        password: this.state.password};
        this.props.sendLogin(urlPath, requireAuth, requestBody)
        }

    handleChange = (event) => {
        if(event.target.placeholder === "Username"){
            this.setState({
                username: event.target.value
            })
        }
        else if(event.target.placeholder === "Password"){
            this.setState({
                password: event.target.value
            }) 
        }
        
    }
    
    render() {
        if(store.getState().loginReducers.isLoggedIn){
            return <Redirect to="/stream"/>
        }
		return(
            <div>
                <h3>Username</h3>
                <div className="ui input">
                    <input type="text" placeholder="Username" onChange={this.handleChange}/>
                </div>
                <h3>Password</h3>
                <div className="ui input">
                    <input type="password" placeholder="Password" onChange={this.handleChange}/>
                </div>
                <br/>
                <button className="ui labeled icon button" id="loginButton" onClick={this.handleRegisterClick}>
                    <i className="user plus icon"></i>
                    Register
                </button>
                <button className="ui labeled icon button" id="loginButton" onClick={this.attemptLogin}>
                    <i className="check icon"></i>
                    Login
                </button>
            </div>
		)
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
export default connect(mapStateToProps, mapDispatchToProps)(LoginFormComponent);