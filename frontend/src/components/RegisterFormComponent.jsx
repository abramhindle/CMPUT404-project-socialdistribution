import React, { Component } from 'react';
import { Form, TextArea } from 'semantic-ui-react';
import PropTypes from 'prop-types';
import { Redirect } from "react-router-dom";
import {connect} from 'react-redux';
import * as RegisterActions from "../actions/RegisterActions";
import "./styles/RegisterFormComponent.css";
class RegisterFormComponent extends Component {	

	constructor(props) {
		super(props);
		this.state = {
            username: "",
            firstName: "",
            lastName: "",
            displayName: "",
            email: "",
            github: "",
            bio: "",
            password: "",
            confirmpassword: "",
            loginAttemps: 0,
		}
	}	
    handleRegisterClick = () => {
        this.props.changePage();
    }

    handleChange = (event) => {
        this.setState({[event.target.name]: event.target.value})
    }

    registerNewUser = () => {
        //console.log(this.state.loginAttemps)
        for (let stateKey in this.state) {
            let htmlElement = document.getElementsByName(stateKey)[0]
            // console.log("Checking textfield "+htmlElement.name)
            if(htmlElement != null && htmlElement.value === "" && (htmlElement.name !== "bio" && htmlElement.name !== "email" && htmlElement.name !== "github" && htmlElement.name !== "firstName" && htmlElement.name !== "lastName")){
                console.log("detected "+stateKey+" was left blank!")
                htmlElement.style.backgroundColor = "red"
            }
        }
        let numLoginAttempts = this.state.loginAttemps
        this.setState({
            loginAttemps: numLoginAttempts+1
        })
        const password = this.state.password
        const confirmpassword = this.state.confirmpassword
        const username = this.state.username
        const displayName = this.state.displayName
        // perform all neccassary validations
        if (password !== confirmpassword) {
            alert("Passwords don't match");
        } 
        else if(username === "" || displayName === "" || password === "" || confirmpassword === ""){
            alert("Required fields are missing.")
        }
        else {
            const requireAuth = false,
            urlPath = "/api/auth/register/",
            requestBody = {username: this.state.username,
                        firstName: this.state.firstName,
                        lastName: this.state.lastName,
                        displayName: this.state.displayName,
                        password: this.state.password,
                        email: this.state.email,
                        github: this.state.github,
                        bio: this.state.bio,
//                        isValid: false,
                    };
            this.props.sendRegister(urlPath, requireAuth, requestBody)
        }
    }

    errorText(props){
        let textBox = document.getElementsByName(props.target.name)
        let enteredValue = textBox
        console.log("Entered with ele: "+enteredValue)
        // if((enteredValue === "" || enteredValue === " ") && this.loginAttemps > 0){
        //     textBox.style.backgroundColor = "red"
        // }
        // else{
        //     enteredValue.style.backgroundColor="white"
        // }
    }

	render() {

		return(
            <div>
                {/* {console.log(this.props)} */}
                {this.props.isValidated && <Redirect push to="/stream" /> }
                <h3>Username *</h3>
                <div className="ui input">
                    <input type="text" name="username" placeholder="Username" onChange={this.handleChange}/>
                </div>
                <h3>Display Name *</h3>
                <div className="ui input">
                    <input type="text" name="displayName" placeholder="Display name" onChange={this.handleChange}/>
                </div>
                <h3>First Name</h3>
                <div className="ui input">
                    <input type="text" name="firstName" placeholder="First name" onChange={this.handleChange}/>
                </div>
                <h3>Last Name</h3>
                <div className="ui input">
                    <input type="text" name="lastName" placeholder="Last name" onChange={this.handleChange}/>
                </div>
                <h3>Email</h3>
                <div className="ui input">
                    <input type="text" name="email" placeholder="Email" onChange={this.handleChange}/>
                </div>
                <h3>Github Profile URL</h3>
                <div className="ui input">
                    <input type="text" name="github" placeholder="Github URL" onChange={this.handleChange}/>
                </div>
                <h3>Bio</h3>
                <Form>
                    <TextArea name="bio" placeholder='Bio'id="BioTexTBox" onChange={this.handleChange}/>
                </Form>
                <h3>Password *</h3>
                <div className="ui input">
                    <input type="password" name="password" placeholder="Password" onChange={this.handleChange}/>
                </div>
                <h3>Confirm Password *</h3>
                <div className="ui input">
                    <input type="password" name="confirmpassword" placeholder="Confirm Password" onChange={this.handleChange}/>
                </div>
                <br/>
                <br/>
                <button className="ui labeled icon button" id="cancelButton" onClick={this.handleRegisterClick}>
                    <i className="close icon"></i>
                    Cancel
                </button>
                <button className="ui labeled icon button" id="registerButton" onClick={this.registerNewUser}>
                    <i className="user plus icon"></i>
                    Confirm
                </button>
                <br/>
            </div>
		)
	}
}

RegisterFormComponent.propTypes = {
    changePage: PropTypes.func.isRequired
};

const mapStateToProps = state => {
    return {
        isValidated: state.registerReducers.isLoggedIn
    }
}

const mapDispatchToProps = dispatch => {
    return {
        sendRegister: (urlPath, requireAuth, requestBody) => {
            return dispatch(RegisterActions.sendRegister(urlPath, requireAuth, requestBody));
        }
    }
}
export default connect(mapStateToProps, mapDispatchToProps)(RegisterFormComponent);