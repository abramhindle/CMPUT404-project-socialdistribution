import React, { Component } from 'react';
import { Input } from 'semantic-ui-react'
import ProfileBubble from './ProfileBubble';
import './PostInput.css';

class PostInput extends Component {	

	constructor(props) {
		super(props);
		this.state = {
		}
	}	

	render() {
	
		return(
			<div className="postInputBoxPosition">
				<div className="postInputBoxBorder">
		        <Input placeholder='What are you thinking about today...?' />
				<button className="ui button"> POST </button>
		    	<button className="ui button"> IMG </button>  
				<ProfileBubble userName={"placeholder"} profilePicture={null} profileBubbleClassAttributes={"ui avatar image"}/>
				</div>
			</div>
		)
	}
}

export default PostInput;