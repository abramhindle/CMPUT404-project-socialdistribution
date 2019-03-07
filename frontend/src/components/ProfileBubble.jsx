import React, { Component } from 'react';
import 'semantic-ui-css/semantic.min.css';
import './styles/ProfileBubble.css';
import {Link} from "react-router-dom";
class ProfileBubble extends Component {	

	constructor(props) {
		super(props);
		this.state = {
		}
	}	

	render() {
		if (this.props.profilePicture) {
			return(
				  	<Link to="/profile" className={this.props.profileBubbleClassAttributes}>
							<img alt={this.props.username} src={this.props.profilePicture}/>		
					</Link>
			)
		}
		else {
			return(
				<Link to="/profile" className={this.props.profileBubbleClassAttributes}>
					<img alt={this.props.username} src={require('../assets/images/default.png')}/>
				</Link>
			)
		}
	}
}

export default ProfileBubble;