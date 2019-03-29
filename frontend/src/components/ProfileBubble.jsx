import React, { Component } from 'react';
import 'semantic-ui-css/semantic.min.css';
import './styles/ProfileBubble.css';
import {Link} from "react-router-dom";
import PropTypes from 'prop-types';

class ProfileBubble extends Component {	

	render() {
		const author_path = "/author/" + encodeURIComponent(this.props.userID);

		let picPath = require('../assets/images/default2.png');
		if (this.props.profilePicture) {
			picPath = this.props.profilePicture;
		}
		return(
				<Link
					to={author_path}
					className={this.props.profileBubbleClassAttributes}
				>
						<span>
							<img alt={this.props.displayName} src={picPath}/>
							<span className="textContainer"> {this.props.displayName.charAt(0)} </span>
						</span>
				</Link>
		);
	}
}

ProfileBubble.propTypes = {
	displayName: PropTypes.string.isRequired,
	userID: PropTypes.string.isRequired,
	profileBubbleClassAttributes: PropTypes.string.isRequired,
	profilePicture: PropTypes.string
};

export default ProfileBubble;