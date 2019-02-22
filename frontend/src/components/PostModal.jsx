import React, { Component } from 'react';
import 'semantic-ui-css/semantic.min.css';
import { Button, Modal, Icon } from 'semantic-ui-react'
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
			title: '',
			description: '',
			content: '',
			username: "Placeholder",
			categories: ["Placeholder"],
			contentType: "text/plain",
		};
		this.handleChange = this.handleChange.bind(this);
		this.handleSubmit = this.handleSubmit.bind(this);
		this.closeModal = this.closeModal.bind(this);
	}	
	
 	closeModal() {
 		console.log(this.state.showModal);
 		this.setState({ showModal: false });
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
		this.closeModal();
	}


	render() {
	
		return(
 				<Modal 
 					trigger={<Button fluid icon onClick={() => this.setState({showModal: true})}> <Icon name="send"/> Create Post </Button>}
					open={this.state.showModal}
					onClose={this.closeModal}
 				>
					<Modal.Header> Create Post </Modal.Header>
					<Modal.Content>
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
						<AnimatedButton iconForButton="pencil icon" buttonText="MD"/> 
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