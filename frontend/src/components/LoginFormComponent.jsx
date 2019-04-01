import React, { Component } from 'react';
import {connect} from 'react-redux';
import * as LoginActions from "../actions/LoginActions";
import { Redirect } from "react-router-dom";
import PropTypes from 'prop-types';
import { Input, Message } from 'semantic-ui-react';
import store from '../store/index.js';
import "./styles/LoginInputText.css";

class LoginFormComponent extends Component {	

	constructor(props) {
		super(props);
		this.state = {
            username: "",
            password: "",
            isLoggedIn: false,
            loginAttempt: 0,
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

        if (store.getState().loginReducers.isLoggedIn === false) {
		    this.setState({
		        loginAttempt: this.state.loginAttempt + 1,
		       	isLoggedIn: store.getState().loginReducers.isLoggedIn,
		    });
        }
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
		return(
            <div>
                {this.props.isValidated && <Redirect push to="/stream" /> }
                {this.props.loginFailure &&
                <Message negative hidden={this.state.loginAttempt === 0}>
                    <Message.Header>Login failed</Message.Header>
                    <p>Please check login details</p>
                </Message>
                }
				
                <h3>Username</h3>
                <Input error={this.state.loginAttempt > 0 && this.props.loginFailure} type="text" placeholder="Username" onChange={this.handleChange} required/>
                <h3>Password</h3>
                <Input error={this.state.loginAttempt > 0 && this.props.loginFailure} type="password" placeholder="Password" onChange={this.handleChange} required/>
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
        isValidated: state.loginReducers.isLoggedIn,
        loginFailure: state.loginReducers.loginFailure,
        
    }
}

const mapDispatchToProps = dispatch => {
    return {
        sendLogin: (urlPath, requireAuth, requestBody) => {
            return dispatch(LoginActions.sendLogin(urlPath, requireAuth, requestBody));
        }
    }
}

LoginFormComponent.propTypes = {
    changePage: PropTypes.func.isRequired
};

export default connect(mapStateToProps, mapDispatchToProps)(LoginFormComponent);