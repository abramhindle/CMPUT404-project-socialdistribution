import React, { Component } from 'react';
import 'semantic-ui-css/semantic.min.css';
import './styles/Login.css';
import RegisterFormComponent from "../components/RegisterFormComponent";
import LoginFormComponent from "../components/LoginFormComponent";
import { Transition } from 'semantic-ui-react'

class Login extends Component {	

	constructor(props) {
		super(props);
		this.state = {
            showLogin: true,
		}
    }	
    
    switchLoginContents = () => {
        const currentPage = this.state.showLogin;

        this.setState({
            showLogin: !currentPage
        });
    }


    shouldRender = () => {
        if (this.state.showLogin) {
            return <LoginFormComponent changePage={this.switchLoginContents}/>
        } else {
            return <RegisterFormComponent changePage={this.switchLoginContents}/>
        }
    }

	render() {
        return(
            <div>
                <h1 id="titleText">GitFriends</h1>
                <Transition visible={this.state.showLogin} animation='pulse' duration={300}>
                    <div id="LoginBox">
                        {this.shouldRender()}
                    </div>
                </Transition>
            </div>
        )
    }
}

export default Login;