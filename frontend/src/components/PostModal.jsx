import React, { Component } from 'react';
import 'semantic-ui-css/semantic.min.css';
import { Button, Modal, Icon, Radio, Transition } from 'semantic-ui-react'
import {connect} from 'react-redux';
import ProfileBubble from './ProfileBubble';
import AnimatedButton from './AnimatedButton';
import Textarea from 'react-textarea-autosize';
import './styles/PostModal.css';

import * as PostActions from "../actions/PostActions";

class PostModal extends Component {	

	constructor(props) {
		super(props);
		this.state = {
			showModal: false,
			
			textContentType: "text/plain",
			imageContentType: '',
			
			title: '',
			description: '',
			content: '',
			username: "Placeholder",
			categories: ["Placeholder"],
		};
		this.handleChange = this.handleChange.bind(this);
		this.handleTextTypeToggle = this.handleTextTypeToggle.bind(this);
		this.handleSubmit = this.handleSubmit.bind(this);
		this.closeModal = this.closeModal.bind(this);
	}	
	
		
 	closeModal() {
 		this.setState({ showModal: false });
	}
	

	handleChange(event) {
		this.setState({[event.target.name]: event.target.value});
	}

	handleTextTypeToggle(event, object) {
		this.setState({textContentType: object.value});
	}

	validPayload(requestBody) {
		if (!(requestBody.title && requestBody.description && requestBody.content)) {
			return false;
		}
		return true;
	}

	handleSubmit(event) {
		const requireAuth = true,
			urlPath = "/api/posts/",
			requestBody = {
				title: this.state.title,
				source: "placeholder",
				origin: "placeholder",
				description: this.state.description,
				contentType: this.state.textContentType + this.state.imageContentType,
				content: this.state.content,
				categories: ["test_category_1"],
				visibility: "PUBLIC",
				visibleTo: [],
				unlisted: false,		
				};
		
		if (this.validPayload(requestBody)) {		
			this.props.sendPost(urlPath, requireAuth, requestBody);
		
			this.setState({
				title: '', 
				description: '', 
				content: '',
				textContentType: "text/plain",
				imageContentType: '',
				});
			this.closeModal();
		}
		
		else {
			alert("Please ensure you have a title, description, and content.");	
		}	
	}


	render() {
	
		return(
 				<Modal 
 					trigger={<Button fluid icon onClick={() => this.setState({showModal: true})}> <Icon name="send"/> Create Post </Button>}
					open={this.state.showModal}
					onClose={this.closeModal}
 				>
					<Modal.Header> Create Post </Modal.Header>
					<Modal.Content className="postModalContent">
					<span className="profileBubbleInModal">
						<ProfileBubble 	userName={"placeholder"} 
									profilePicture={null} 
									profileBubbleClassAttributes={"ui circular bordered small image"}
						/>
					</span>
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
										minRows={2}
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
										minRows={4}
										value={this.state.content}
										onChange={this.handleChange}
							/>
						</div>
						</Modal.Content>
						<Modal.Actions>
							<AnimatedButton iconForButton="image icon" buttonText="IMG"/> 
							<Radio toggle name='textTypeGroup' value='text/plain' label="Plain Text" checked={this.state.textContentType === 'text/plain'} className="textToggle" onClick={this.handleTextTypeToggle}/>
							<Radio toggle name='textTypeGroup' value='text/markdown' label="Markdown" checked={this.state.textContentType === 'text/markdown'} className="textToggle" onClick={this.handleTextTypeToggle}/>
							<Radio toggle name='textTypeGroup' value='application/base64' label="Base 64" checked={this.state.textContentType === 'application/base64'} className="textToggle" onClick={this.handleTextTypeToggle}/>
							<AnimatedButton iconForButton="play icon" buttonText="POST" clickFunction={this.handleSubmit}/>
						</Modal.Actions>
				</Modal>
	)}
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


export default connect(mapStateToProps, mapDispatchToProps)(PostModal);