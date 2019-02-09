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
		if (this.props.sideBar) {
			if (this.props.profilePicture) {
				return(
					<img className={this.props.profileBubbleClassAttributes} alt={this.props.userName} src={this.props.profilePicture}/>		
				)
			}
			else {
				return( 
					<img className={this.props.profileBubbleClassAttributes} alt={this.props.userName} src={require('../assets/images/default.png')}/>
				)
			}
		}


		if (this.props.profilePicture) {
			return(
				  	<a href="https://google.com" className={this.props.profileBubbleClassAttributes}>
							<img alt={this.props.userName} src={this.props.profilePicture}/>		
					</a>
			)
		}
		else {
			return(
				<a href="https://google.com" className={this.props.profileBubbleClassAttributes}>
					<img alt={this.props.userName} src={require('../assets/images/default.png')}/>
				</a>
			)
		}
	}
}

export default ProfileBubble;