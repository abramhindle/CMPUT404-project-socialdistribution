import React, { Component } from 'react';
import 'semantic-ui-css/semantic.min.css';
import './styles/ProfileBubble.css'
class ProfileBubble extends Component {	

	constructor(props) {
		super(props);
		this.state = {
		}
	}	

	render() {
		if (this.props.profilePicture) {
			return(
				  	<a href="https://google.com" className={this.props.profileBubbleClassAttributes}>
							<img alt={this.props.username} src={this.props.profilePicture}/>		
					</a>
			)
		}
		else {
			return(
				<a href="https://google.com" className={this.props.profileBubbleClassAttributes}>
					<img alt={this.props.username} src={require('../assets/images/default.png')}/>
				</a>
			)
		}
	}
}

export default ProfileBubble;