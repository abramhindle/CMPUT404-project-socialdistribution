import React, { Component } from 'react';
import 'semantic-ui-css/semantic.min.css';
import { Button, Modal, Icon, Checkbox } from 'semantic-ui-react'
import {connect} from 'react-redux';
import ProfileBubble from './ProfileBubble';
import AnimatedButton from './AnimatedButton';
import VisibilitySettings from './VisibilitySettings';
import TextTypeSettings from './TextTypeSettings';
import CategoriesModal from './CategoriesModal';
import Textarea from 'react-textarea-autosize';
import './styles/CreatePostModal.css';

import * as PostActions from "../actions/PostActions";

class CreatePostModal extends Component {		

	constructor(props) {
		super(props);
		this.state = {
			showModal: false,
			
			textContentType: "text/plain",
			imageContentType: '',
			
			file: '',
			imagePreviewUrl: '',
			
			createPostPageOne: true,
			
			title: '',
			description: '',
			content: '',
			username: "Placeholder",
			categories: [],
			visibility: "PUBLIC",
			visibleTo: [],
			unlisted: false,
		};
		this.handleChange = this.handleChange.bind(this);
		this.handleUnlistedCheck = this.handleUnlistedCheck.bind(this);
		this.handleDropdownChanges = this.handleDropdownChanges.bind(this);
		this.handleCategoryChange = this.handleCategoryChange.bind(this);
		
		this.switchPages = this.switchPages.bind(this);
		
		this.clearForm = this.clearForm.bind(this);
		this.clearContent = this.clearContent.bind(this);
		this.handleSubmit = this.handleSubmit.bind(this);
		this.closeModal = this.closeModal.bind(this);
	}	
	
		
 	closeModal() {
 		this.setState({ showModal: false, createPostPageOne: true, });
	}
	

	handleChange(event) {
		this.setState({[event.target.name]: event.target.value});
	}

	handleUnlistedCheck() {
		this.setState({unlisted: !this.state.unlisted});
	}

	handleDropdownChanges(name, event) {
		this.setState({[name]: event.value});
	}

	handleCategoryChange(newCategories) {
		this.setState({
		  categories: newCategories,
		})
	}

	switchPages() {
		this.setState({
			createPostPageOne: !this.state.createPostPageOne,
		});
	}

	handleImageChange(e) {
		e.preventDefault();

		let reader = new FileReader();
		let file = e.target.files[0];

		reader.onloadend = () => {
			this.setState({
				file: file,
				imagePreviewUrl: reader.result
			});
		}

		reader.readAsDataURL(file)
	}

	clearForm() {
		this.setState({
			title: '', 
			description: '', 
			content: '',
			categories: [],
			file: '',
			textContentType: "text/plain",
			imageContentType: '',
			imagePreviewUrl: '',
			});
	}

	clearContent() {
		this.setState({
			content: '',
			file: '',
			imageContentType: '',
			imagePreviewUrl: '',
			});
	}

	validPayload(requestBody) {
		if (!(requestBody.title && requestBody.description && requestBody.content && requestBody.categories.length > 0)) {
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
				categories: this.state.categories,
				visibility: this.state.visibility,
				visibleTo: this.state.visibleTo,
				unlisted: this.state.unlisted,		
				};
		
		if (this.validPayload(requestBody)) {		
			this.props.sendPost(urlPath, requireAuth, requestBody);
		
			this.setState({
				title: '', 
				description: '', 
				content: '',
				textContentType: "text/plain",
				imageContentType: '',
				categories: [],
				file: '',
				imagePreviewUrl: '',
				});
			this.closeModal();
		}
		
		else {
			alert("Please ensure you have a title, description, categories, and content.");	
		}	
	}


	render() {
		
		let {imagePreviewUrl} = this.state;
		let $imagePreview = null;
		if (imagePreviewUrl) {
			$imagePreview = (<img className="imgPreview" src={imagePreviewUrl} alt="A preview of what you uploaded"/>);
		}
		
	
		return(
 				<Modal 
 					trigger={<Button fluid icon onClick={() => this.setState({showModal: true})}> <Icon name="send"/> Create Post </Button>}
					open={this.state.showModal}
					onClose={this.closeModal}
 					className={"createPostModal"}
 				>
					<Modal.Header className='createPostHeader'> Create Post </Modal.Header>
					<Modal.Content className="postModalContent">
					
					{this.state.createPostPageOne ?
					<span>
					<span className="profileBubbleInModal">
						<ProfileBubble 	userName={"placeholder"} 
									profilePicture={null} 
									profileBubbleClassAttributes={"ui circular bordered small image"}
						/>
					</span>
						<div className="titleDescriptionContainer">
							<Textarea 	
										name="title"
										className="titleInputBox" 
										placeholder="Title..."
										minRows={1}
										maxLength="45"
										value={this.state.title}
										onChange={this.handleChange}
							/>

							<Textarea 	
										name="description"
										className="descriptionInputBox" 
										placeholder="Describe your post..."
										minRows={5}
										maxRows={7}
										maxLength="300"
										value={this.state.description}
										onChange={this.handleChange}
							/>
							<br/>
						</div>
						</span>
						
						:
						<div className="fullContentContainer">
							<Textarea 	
										name="content"
										className="contentTextBox" 
										placeholder="What's your post about?"
										minRows={6}
										value={this.state.content}
										onChange={this.handleChange}
							/>
							<span>{$imagePreview}</span>
						</div>
						}
						
						</Modal.Content>
						<Modal.Actions>
							{this.state.createPostPageOne 
							?
							<span>
							<span className="nonContentSettings">
							<Checkbox label='unlisted' name="unlisted" toggle onChange={this.handleUnlistedCheck} checked={this.state.unlisted} className="unlistedCheckboxContainer" />
							<VisibilitySettings visibility={this.state.visibility} handleChange={this.handleDropdownChanges} /> 
							<TextTypeSettings handleChange={this.handleDropdownChanges} />
							<CategoriesModal currentValues={this.state.categories} handleCategoryChange={this.handleCategoryChange}/>
							</span>
							<AnimatedButton iconForButton="angle double right icon" buttonText="NEXT" clickFunction={this.switchPages}/>
							</span>
							:
							<span>
							
							<span className="backButton">
							<AnimatedButton iconForButton="angle double left icon" buttonText="BACK" clickFunction={this.switchPages}/>
							</span>
							
							<span>
							<label htmlFor="imageUploadFile">
							<AnimatedButton iconForButton="image icon" buttonText="IMG"/>
							</label>
							<input type="file" id="imageUploadFile" accept="image/png, image/jpeg" onChange={(e)=>this.handleImageChange(e)} style={{display: 'none'}}/>
							</span>
							
							<AnimatedButton iconForButton="play icon" buttonText="POST" clickFunction={this.handleSubmit}/>
							</span>
							}
							
						</Modal.Actions>
				</Modal>
	)}
}

const mapStateToProps = state => {
    return {
        state: state.isLoggedIn,
    }
}

const mapDispatchToProps = dispatch => {
    return {
        sendPost: (urlPath, requireAuth, requestBody) => {
            return dispatch(PostActions.sendPost(urlPath, requireAuth, requestBody));
        }
    }
}


export default connect(mapStateToProps, mapDispatchToProps)(CreatePostModal);