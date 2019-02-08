import React, { Component } from 'react';
import 'semantic-ui-css/semantic.min.css';
import SideBar from '../components/SideBar';

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
				<h1> This is a test. AHHHHHHHHHHHHHH </h1>
			</div>
		  </div>
	)
}
}

export default Stream;