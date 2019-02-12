import React, { Component } from 'react';
import 'semantic-ui-css/semantic.min.css';
import ProfileBubble from './ProfileBubble';
import AnimatedButton from './AnimatedButton';
import './styles/PostInput.css';

class PostInput extends Component {	

	constructor(props) {
		super(props);
		this.state = {
		}
	}	

	render() {
	
		return(
			<div className="postInputBoxPosition">
				<span className="postInputBoxBorder">
					<AnimatedButton iconForButton="image icon" buttonText="IMG"/> 
					<textarea 	className="postInputBoxTextArea" 
								placeholder="What are you thinking about today?"
								rows="1">
					</textarea>
					<AnimatedButton iconForButton="pencil icon" buttonText="MD"/> 
					<AnimatedButton iconForButton="play icon" buttonText="POST"/>
				</span>
				<ProfileBubble 	userName={"placeholder"} 
				profilePicture={null} 
				profileBubbleClassAttributes={"ui circular bordered tiny image"}/>
			</div>
		)
	}
}

export default PostInput;