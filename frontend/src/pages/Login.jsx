import React, { Component } from 'react';
import 'semantic-ui-css/semantic.min.css';
import ProfileBubble from "../components/ProfileBubble";
import LoginInputText from "../components/LoginInputText";
class Login extends Component {	

	constructor(props) {
		super(props);
		this.state = {
		}
	}	

	render() {
        return(
            <div>		
                <LoginInputText message="John is cool" apples="orange"/>
            </div>
        )
    }
}

export default Login;