import React, { Component } from 'react';
import { Input } from 'semantic-ui-react';

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

export default RegisterFormComponent;