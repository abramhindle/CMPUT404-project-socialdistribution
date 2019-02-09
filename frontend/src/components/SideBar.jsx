import React, { Component } from 'react';
import 'semantic-ui-css/semantic.min.css';
import ProfileBubble from './ProfileBubble';
import './SideBar.css';

class SideBar extends Component {	

	constructor(props) {
		super(props);
		this.state = {
		}
	}	

	render() {
		return(
			<div className="ui left fixed vertical inverted sidebar labeled icon menu blue visible sideBarMenu">		
				<a href="https://google.com" className="item sideBarProfile">
					<ProfileBubble 	
									userName={"placeholder"} 
									profilePicture={null} 
									profileBubbleClassAttributes={"ui circular tiny bordered centered image"}
									sideBar={true}
														
					/>

				  	<figcaption>Profile</figcaption>
				</a>

				<a href="https://google.com" className="item sideBarItem">
					<i className="tint icon"></i>
				  	Stream
				</a>

				<a href="https://google.com" className="item sideBarItem">
					<i className="users icon"></i>
				 	 Friends
				</a>
				<a href="https://google.com" className="item sideBarItem">
					<i className="globe icon"></i>
				  	Public
				</a>
				<a href="https://google.com" className="item sideBarItem">
					<i className="sign-out icon"></i>
				  	Logout
				</a>

			</div>
		)
	}
}

export default SideBar;