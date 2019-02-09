import React, { Component } from 'react';
import 'semantic-ui-css/semantic.min.css';
import './ProfileBubble.css'
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
							<img className="profileBubbleBorder" src={this.props.profilePicture}/>		
					</a>
			)
		}
		else {
			return(
				<a href="https://google.com" className={this.props.profileBubbleClassAttributes}>
					<img className="profileBubbleBorder" src={require('../assets/images/default.png')}/>
				</a>
			)
		}
	}
}

export default ProfileBubble;