import React, { Component } from 'react';
import { Input } from 'semantic-ui-react'
import {connect} from 'react-redux';
import * as LoginActions from "../actions/LoginActions";
import { Redirect } from "react-router-dom";
import PropTypes from 'prop-types';


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
		return(
            <div>
                {this.props.isValidated && <Redirect push to="/stream" /> }
                <h3>Username</h3>
                <div className="ui input">
                    <input type="text" placeholder="Username" onChange={this.handleChange} required/>
                </div>
                <h3>Password</h3>
                <div className="ui input">
                    <input type="password" placeholder="Password" onChange={this.handleChange} required/>
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
        isValidated: state.loginReducers.isLoggedIn
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