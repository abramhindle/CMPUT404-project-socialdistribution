import React, { Component } from 'react';
import { Form, TextArea } from 'semantic-ui-react';
import PropTypes from 'prop-types';
import "./styles/RegisterFormComponent.css";
class RegisterFormComponent extends Component {	

	constructor(props) {
		super(props);
		this.state = {
		}
	}	
    handleRegisterClick = () => {
        this.props.changePage();
    }

    registerNewUser = () => {

    }
	render() {

		return(
            <div>
                <h3>Username</h3>
                <div className="ui input">
                    <input type="text" placeholder="Username"/>
                </div>
                <h3>Email</h3>
                <div className="ui input">
                    <input type="text" placeholder="Email"/>
                </div>
                <h3>Github Profile URL</h3>
                <div className="ui input">
                    <input type="text" placeholder="Github URL"/>
                </div>
                <h3>Bio</h3>
                <Form>
                    <TextArea placeholder='Bio'id="BioTexTBox"/>
                </Form>
                <h3>Password</h3>
                <div className="ui input">
                    <input type="password" placeholder="Password"/>
                </div>
                <h3>Confirm Password</h3>
                <div className="ui input">
                    <input type="password" placeholder="Confirm Password"/>
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

export default RegisterFormComponent;