import React, { Component } from 'react';
import 'semantic-ui-css/semantic.min.css';
import './styles/ProfileBubble.css';
import {Link} from "react-router-dom";
import PropTypes from 'prop-types';
import utils from "../util/utils";

class ProfileBubble extends Component {	

	render() {
		const author_path = "/author/" + utils.getStripedEscapedAuthorId(this.props.userID);

		let picPath = require('../assets/images/default.png');
		if (this.props.profilePicture) {
			picPath = this.props.profilePicture;
		}
		return(
				<Link
					to={{pathname: author_path,
						  state: {
							fullAuthorId: this.props.userID
						  }
						}}
					className={this.props.profileBubbleClassAttributes}
				>
						<img alt={this.props.username} src={picPath}/>
				</Link>
		);
	}
}

ProfileBubble.propTypes = {
	username: PropTypes.string.isRequired,
	userID: PropTypes.string.isRequired,
	profileBubbleClassAttributes: PropTypes.string.isRequired,
	profilePicture: PropTypes.string
};

export default ProfileBubble;