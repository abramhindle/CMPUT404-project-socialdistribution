import React, { Component } from 'react';
import 'semantic-ui-css/semantic.min.css';
import {connect} from 'react-redux';
import Textarea from 'react-textarea-autosize';
import ProfileBubble from './ProfileBubble';
import AnimatedButton from './AnimatedButton';
import './styles/PostInput.css';

import * as PostActions from "../actions/PostActions";

class PostInput extends Component {	

	constructor(props) {
		super(props);
		this.state = {
			title: '',
			description: '',
			content: '',
			username: "Placeholder",
			categories: ["Placeholder"],
			contentType: "text/plain",
		};
		this.handleChange = this.handleChange.bind(this);
		this.handleSubmit = this.handleSubmit.bind(this);
	}	

	handleChange(event) {
		this.setState({[event.target.name]: event.target.value});
	}

	handleSubmit(event) {
		var currentDateTime = new Date();
		const requireAuth = true,
			urlPath = "/api/post/",
			requestBody = {
				title: this.state.title,
				description: this.state.description,
				content: this.state.content,
				author: this.state.username,
				categories: this.state.categories,
				publishedDateTime: currentDateTime,
				contentType: this.state.contentType,
				privacySettings: {},		
				};
			this.props.sendPost(urlPath, requireAuth, requestBody);
	
	
		this.setState({
			title: '', 
			description: '', 
			content: ''});
	}


	render() {
	
		return(
			<div className="postInputPosition">
				<span className="postInputBoxBorder">
					<AnimatedButton iconForButton="image icon" buttonText="IMG"/> 
					<div className="postInputTextAreaContainer">
						<Textarea 	
									name="title"
									className="postInputBoxTextArea" 
									placeholder="Title"
									maxRows={1}
									maxLength="45"
									value={this.state.title}
									onChange={this.handleChange}
									/>
						<br/>
						<Textarea 	
									name="description"
									className="postInputBoxTextArea" 
									placeholder="Description"
									maxRows={2}
									maxLength="100"
									value={this.state.description}
									onChange={this.handleChange}
									/>
						<br/>
						<Textarea 	
									name="content"
									className="postInputBoxTextArea" 
									placeholder="What are you thinking about today?"
									minRows={2}
									value={this.state.content}
									onChange={this.handleChange}
									/>
					</div>
					<span>
						<label htmlFor="imageUpload">
						<AnimatedButton iconForButton="pencil icon" buttonText="MD"/> 
						</label>
						<input type="file" name="imageUpload" style={{display: 'none',}}/>
					</span>
					<AnimatedButton iconForButton="play icon" buttonText="POST" clickFunction={this.handleSubmit}/>
				</span>
				<ProfileBubble 	userName={"placeholder"} 
				profilePicture={null} 
				profileBubbleClassAttributes={"ui circular bordered tiny image"}/>
			</div>
		)
	}
}

const mapStateToProps = state => {
    return {
        state: state.isLoggedIn
    }
}

const mapDispatchToProps = dispatch => {
    return {
        sendPost: (urlPath, requireAuth, requestBody) => {
            return dispatch(PostActions.sendPost(urlPath, requireAuth, requestBody));
        }
    }
}


export default connect(mapStateToProps, mapDispatchToProps)(PostInput);