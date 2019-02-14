import React, { Component } from 'react';
import 'semantic-ui-css/semantic.min.css';
import PostInput from '../components/PostInput';

class Stream extends Component {	

	constructor(props) {
		super(props);
		this.state = {
		}
	}	

	render() {
	return(	
		<div className="pusher">
			<h1> This is where we put the stuff for the Stream page</h1>
			<PostInput/>
		</div>
	    )
    }
}



export default Stream;
