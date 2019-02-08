import React, { Component } from 'react';
import 'semantic-ui-css/semantic.min.css';
import './SideBar.css';

class SideBar extends Component {	

	constructor(props) {
		super(props);
		this.state = {
		}
	}	

	render() {
	return(
		  <div class="ui left fixed vertical inverted sidebar labeled icon menu blue visible sideBarMenu">		
			<a class="item sideBarItem">
				<i class="user circle icon"></i>
			  	Profile
			</a>

			<a class="item sideBarItem">
				<i class="tint icon"></i>
			  	Stream
			</a>

			<a class="item sideBarItem">
				<i class="user circle icon"></i>
			 	 Friends
			</a>
			<a class="item sideBarItem">
				<i class="globe icon"></i>
			  	Public
			</a>
			<a class="item sideBarItem">
				<i class="sign-out icon"></i>
			  	Logout
			</a>

		  </div>
	)
}
}

export default SideBar;