import React, { Component } from 'react';
import 'semantic-ui-css/semantic.min.css';
import './styles/ProfileBubble.css';
import {Link} from "react-router-dom";
import PropTypes from 'prop-types';

class ProfileBubble extends Component {	

	render() {
		let $userID = this.props.userID.split('/').pop();
	
		if (this.props.profilePicture === "$No profile picture provided") {
			return(
				  	<Link to={$userID} className={this.props.profileBubbleClassAttributes}>
							<img alt={this.props.username} src={this.props.profilePicture}/>		
					</Link>
			)
		}
		else {
			return(
				<Link to={$userID} className={this.props.profileBubbleClassAttributes}>
					<img alt={this.props.username} src={require('../assets/images/default.png')}/>
				</Link>
			)
		}
	}
}

ProfileBubble.defaultProps = {
	// A unique $tring to indicate we're using the default profile picture here. 
	profilePicture: '$No profile picture provided'
}

ProfileBubble.propTypes = {
	username: PropTypes.string.isRequired,
	userID: PropTypes.string.isRequired,
	profileBubbleClassAttributes: PropTypes.string.isRequired,
};

export default ProfileBubble;