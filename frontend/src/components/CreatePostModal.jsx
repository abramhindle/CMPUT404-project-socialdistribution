import React, { Component } from 'react';
import 'semantic-ui-css/semantic.min.css';
import { Button, Modal, Icon, Checkbox, TextArea, Form, Input } from 'semantic-ui-react';
import {connect} from 'react-redux';
import ProfileBubble from './ProfileBubble';
import AnimatedButton from './AnimatedButton';
import VisibilitySettings from './VisibilitySettings';
import CategoriesModal from './CategoriesModal';
import './styles/CreatePostModal.css';

import * as PostActions from "../actions/PostActions";

class CreatePostModal extends Component {		

	constructor(props) {
		super(props);
		this.state = {
			showModal: false,
			
			contentType: "text/plain",
			//textContentType: "text/plain",
			//imageContentType: '',
			
			file: '',
			imagePreviewUrl: '',
			
			createPostPageOne: true,
			
			title: '',
			description: '',
			content: '',
			username: '',
			categories: [],
			visibility: "PUBLIC",
			visibleTo: [],
			unlisted: false,
		};
		this.handleChange = this.handleChange.bind(this);
		this.handleUnlistedCheck = this.handleUnlistedCheck.bind(this);
		this.handleDropdownChanges = this.handleDropdownChanges.bind(this);
		this.handleMarkdownToggle = this.handleMarkdownToggle.bind(this);
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
		if (this.state.visibility !== "PUBLIC") {
			alert("Unlisted posts are always PUBLIC. Your visibility settings will be changed");
		}
		this.setState({
		unlisted: !this.state.unlisted,
		visibility: "PUBLIC",
		});
	}

	handleMarkdownToggle() {
		if (this.state.contentType === 'text/markdown') {
			this.setState({
				contentType: 'text/plain',
			});
		}
		else {
			this.setState({
				contentType: 'text/markdown',
			});
		}
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
				content: reader.result,
				//imageContentType: file.type + ";base64",
				contentType: file.type + ";base64", 
				imagePreviewUrl: reader.result,
			});
		};
		reader.readAsDataURL(file);
	}

	clearForm() {
		this.setState({
			title: '', 
			description: '', 
			content: '',
			categories: [],
			file: '',
			//textContentType: "text/plain",
			//imageContentType: '',
			contentType: "text/plain",
			imagePreviewUrl: '',
			});
	}

	clearContent() {
		this.setState({
			content: '',
			file: '',
			contentType: "text/plain",
			//imageContentType: '',
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
				
				//contentType: this.state.textContentType + this.state.imageContentType,
				contentType: this.state.contentType,
				
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
				//textContentType: "text/plain",
				//imageContentType: '',
				contentType: "text/plain",
				categories: [],
				file: '',
				imagePreviewUrl: '',
				unlisted: false,
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
					<Modal.Header className='createPostHeader'> <h3> Create Post </h3> </Modal.Header>
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
							<Form>
							<Input 	
										name="title"
										className="titleInputBox" 
										placeholder="TITLE..."
										size="small"
										value={this.state.title}
										onChange={this.handleChange}
							/>

							<TextArea
										name="description"
										className="descriptionInputBox" 
										placeholder="Describe your post..."
										rows="3"
										value={this.state.description}
										onChange={this.handleChange}
							/>
							</Form>
							<br/>
						</div>
						</span>
						
						:
						<div>
							{this.state.file === ''
							?
							<Form>
							<TextArea	
										name="content"
										className="contentTextBox" 
										placeholder="What's your post about?"
										rows="6"
										autoHeight
										value={this.state.content}
										onChange={this.handleChange}
							/>
							</Form>
							:
							<span>{$imagePreview}</span>
							}
							
						</div>
						}
						
						</Modal.Content>
						<Modal.Actions>
							{this.state.createPostPageOne 
							?
							<span>
							<span className="nonContentSettings">
							<VisibilitySettings visibility={this.state.visibility} userID={this.props.userID} handleChange={this.handleDropdownChanges} unlisted={this.state.unlisted} /> 
							<CategoriesModal currentValues={this.state.categories} handleCategoryChange={this.handleCategoryChange} />
							</span>
							<AnimatedButton iconForButton="angle double right icon" buttonText="NEXT" clickFunction={this.switchPages}/>
							</span>
							:
							<span>
							
							<span className="backButton">
							<AnimatedButton iconForButton="angle double left icon" buttonText="BACK" clickFunction={this.switchPages}/>
							</span>
							<Checkbox label='unlisted' name="unlisted" toggle onChange={this.handleUnlistedCheck} checked={this.state.unlisted} className="toggleContainer" />
							<Checkbox label='Markdown' name="contentType" toggle onChange={this.handleMarkdownToggle} checked={this.state.contentType === 'text/markdown'} disabled={this.state.file !== ''}  className='toggleContainer'/>     
							
							<AnimatedButton iconForButton="trash alternate outline icon" buttonText="Clear" clickFunction={this.clearContent}/>
							
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
    	userID: state.userID,
        username: state.username,
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