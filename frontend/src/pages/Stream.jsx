import React, { Component } from 'react';
import 'semantic-ui-css/semantic.min.css';
import SideBar from '../components/SideBar';
import PostInput from '../components/PostInput';

class Stream extends Component {	

	constructor(props) {
		super(props);
		this.state = {
		}
	}	

	render() {
	return(
		  <div>		
			<SideBar/>
			<div class="pusher">
				<div>
				<h1> This is where we put the stuff for the current page</h1>
				<PostInput/>
				</div>
			</div>
		  </div>
	)
}
}

export default Stream;