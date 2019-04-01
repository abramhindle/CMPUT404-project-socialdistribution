import React, { Component } from 'react';
import { Form, TextArea, Input, Message} from 'semantic-ui-react';
import PropTypes from 'prop-types';
import HTTPFetchUtil from "../util/HTTPFetchUtil";
import "./styles/RegisterFormComponent.css";
import AbortController from 'abort-controller';


const controller = new AbortController();
const signal = controller.signal;
signal.addEventListener("abort", () => {});

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
            error: false,
		}
    }	
    
    handleRegisterClick = () => {
        this.props.changePage();
    }

    handleChange = (event) => {
        this.setState({[event.target.name]: event.target.value})
    }

    registerNewUser = () => {
        let numLoginAttempts = this.state.loginAttemps
        this.setState({
            loginAttemps: numLoginAttempts+1
        })
        // perform all neccassary validations
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
                };
                
		 HTTPFetchUtil.sendPostRequest(urlPath, requireAuth, requestBody, signal)
				    .then((httpResponse) => {
				        if (httpResponse.status === 200) {
				            httpResponse.json().then((results) => {
				            	this.props.changePage();
				            })
				        }
				        else {
				        	this.setState({
				        		error: true,
				        	});
				        }
				})
				.catch((error) => {
					console.error(error);
				});
	}

	render() {

		return(
            <div>
            	{this.state.error && 
                <Message negative hidden={this.state.loginAttemps === 0}>
                    <Message.Header>Registration failed</Message.Header>
                    <p>Please check required fields and try again</p>
                </Message>
                }
                <h3>Username *</h3>
                <Input type="text" name="username" placeholder="Username" onChange={this.handleChange}/>
                <h3>Display Name *</h3>
                <Input type="text" name="displayName" placeholder="Display name" onChange={this.handleChange}/>
                <h3>First Name</h3>
                <Input type="text" name="firstName" placeholder="First name" onChange={this.handleChange}/>
                <h3>Last Name</h3>
                <Input type="text" name="lastName" placeholder="Last name" onChange={this.handleChange}/>
                <h3>Email</h3>
                <Input type="text" name="email" placeholder="Email" onChange={this.handleChange}/>
                <h3>Github Profile URL</h3>
                <Input type="text" name="github" placeholder="Github URL" onChange={this.handleChange}/>
                <h3>Bio</h3>
                <Form>
                    <TextArea name="bio" placeholder='Bio'id="BioTexTBox" onChange={this.handleChange}/>
                </Form>
                <h3>Password *</h3>
                <Input type="password" name="password" placeholder="Password" onChange={this.handleChange}/>
                <h3>Confirm Password *</h3>
                <Input type="password" name="confirmpassword" placeholder="Confirm Password" onChange={this.handleChange}/>
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

export default RegisterFormComponent;