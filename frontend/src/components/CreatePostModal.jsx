import React, { Component } from 'react';
import { Modal, Checkbox, TextArea, Form, Input } from 'semantic-ui-react';
import {connect} from 'react-redux';
import ProfileBubble from './ProfileBubble';
import AnimatedButton from './AnimatedButton';
import VisibilitySettings from './VisibilitySettings';
import CategoriesModal from './CategoriesModal';
import HTTPFetchUtil from "../util/HTTPFetchUtil";
import PropTypes from 'prop-types';
import Cookies from 'js-cookie';
import './styles/CreatePostModal.css';


class CreatePostModal extends Component {		

	constructor(props) {
		super(props);
		this.state = {
			file: '',
			imagePreviewUrl: '',
			
			createPostPageOne: true,
			
			title: this.props.title,
			description: this.props.description,
			content: this.props.content,
			contentType: this.props.contentType,
			categories: this.props.categories,
			visibility: this.props.visibility,
			visibleTo: this.props.visibleTo,
			unlisted: this.props.unlisted,
		};
		
		this.handleChange = this.handleChange.bind(this);
		this.handleUnlistedCheck = this.handleUnlistedCheck.bind(this);
		this.handleDropdownChanges = this.handleDropdownChanges.bind(this);
		this.handleMarkdownToggle = this.handleMarkdownToggle.bind(this);
		this.handleCategoryChange = this.handleCategoryChange.bind(this);
		
		this.switchPages = this.switchPages.bind(this);
		this.createPageOneOrPageTwoButtons = this.createPageOneOrPageTwoButtons.bind(this);
		
		this.clearForm = this.clearForm.bind(this);
		this.clearContent = this.clearContent.bind(this);
		this.handleSubmit = this.handleSubmit.bind(this);
		this.closeModal = this.closeModal.bind(this);
	}	
	
	componentDidMount() {
		if (this.state.contentType === "image/png;base64" || this.state.contentType === "image/jpeg;base64") {
			if (this.state.file === '') {
				this.setState({
					imagePreviewUrl: this.state.content,
				});
			}		
		}
	}
		
 	closeModal() {
 		if (this.props.isEdit) {
 		this.setState({
 			createPostPageOne: true,
 			title: this.props.title,
			description: this.props.description,
			content: this.props.content,
			contentType: this.props.contentType,
			categories: this.props.categories,
			visibility: this.props.visibility,
			visibleTo: this.props.visibleTo,
			unlisted: this.props.unlisted,
 		});
 		}
 		else {
 			this.setState({
 				createPostPageOne: true,
 			});
 		}
 		
 		this.props.closeModal();
	}
	

	handleChange(event) {
		this.setState({[event.target.name]: event.target.value});
	}

	handleUnlistedCheck(event) {
		event.stopPropagation();
		this.setState({
		unlisted: !this.state.unlisted,
		});
	}

	handleMarkdownToggle(event) {
		event.stopPropagation();
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

	switchPages(event) {
		event.stopPropagation();
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
			contentType: "text/plain",
			imagePreviewUrl: '',
			});
	}

	clearContent() {
		this.setState({
			content: '',
			file: '',
			contentType: "text/plain",
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
		const requireAuth = true;
		const requestBody = {
				title: this.state.title,
				description: this.state.description,
				contentType: this.state.contentType,
				content: this.state.content,
				categories: this.state.categories,
				visibility: this.state.visibility,
				visibleTo: this.state.visibleTo,
				unlisted: this.state.unlisted,		
				};
		
		if (this.validPayload(requestBody)) {		
			let urlPath;
			if (this.props.isEdit) {
				urlPath = "/api/posts/" + this.props.postID;
				HTTPFetchUtil.sendPutRequest(urlPath, requireAuth, requestBody)
				    .then((httpResponse) => {
				        if (httpResponse.status === 200) {
							this.props.getPosts();	
							this.props.closeModal();
							this.setState({
								createPostPageOne: true,
							});
							alert("Edited post successfully!");	
				        }
				        else {
				        	alert("Failed to edit post");
							this.setState({
								createPostPageOne: true,
							});
				        }
				    })
				    .catch((error) => {
				        console.error(error);
				});
			}
			else {
				urlPath = "/api/posts/";
				HTTPFetchUtil.sendPostRequest(urlPath, requireAuth, requestBody)
				    .then((httpResponse) => {
				        if (httpResponse.status === 200) {
							this.props.getPosts();	
							this.props.closeModal();
							this.setState({
								title: '', 
								description: '', 
								content: '',
								contentType: "text/plain",
								categories: [],
								file: '',
								imagePreviewUrl: '',
								unlisted: false,
								createPostPageOne: true,
							});	
							alert("Created post successfully!");	
				        }
				        else {
				        	alert("Failed to create post");
							this.setState({
								createPostPageOne: true,
							});
				        }
				    })
				    .catch((error) => {
				        console.error(error);
					});
			}
		}
		else {
			alert("Please ensure you have a title, description, categories, and content.");	
		}	
	}

	createPageOneOrPageTwoButtons() {
		if (this.state.createPostPageOne) { 
			return(
				<span>
				<span className="nonContentSettings">
				<VisibilitySettings visibility={this.state.visibility} userID={Cookies.get("userID").split('/').pop() || this.props.storeItems.userId.split('/').pop()} handleChange={this.handleDropdownChanges}/> 
				<CategoriesModal currentValues={this.state.categories} handleCategoryChange={this.handleCategoryChange} />
				</span>
				<AnimatedButton iconForButton="angle double right icon" buttonText="NEXT" clickFunction={this.switchPages}/>
				</span>
			)
		}
		else {
			return(
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

				<AnimatedButton iconForButton="checkmark icon" buttonText="CONFIRM" clickFunction={this.handleSubmit}/>
				</span>
			)
		}
	}

	render() {
		let {imagePreviewUrl} = this.state;
		let $imagePreview = null;
		if (imagePreviewUrl) {
			$imagePreview = (<img className="imgPreview" src={imagePreviewUrl} alt="A preview of what you uploaded"/>);
		}
		
		let $modalHeader = (<h3>Create Post</h3>);
		if (this.props.isEdit) {
			$modalHeader = (<h3>Edit Post</h3>);
		}
	
		return(
 				<Modal 
 					trigger={this.props.modalTrigger}
					open={this.props.showModal}
					onClose={this.closeModal}
 					className={"createPostModal"}
 				>
					<Modal.Header className='createPostHeader'> {$modalHeader} </Modal.Header>
					<Modal.Content className="postModalContent">
					
					{this.state.createPostPageOne ?
					<span>
					<span className="profileBubbleInModal">
						<ProfileBubble
							username={this.props.storeItems.username || Cookies.get("username")}
							userID={this.props.storeItems.userID || Cookies.get("userID")}
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
							{this.state.imagePreviewUrl === ''
							?
							<Form>
							<TextArea	
										name="content"
										className="contentTextBox" 
										placeholder="What's your post about?"
										rows="6"
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
						{this.createPageOneOrPageTwoButtons()}
						</Modal.Actions>
				</Modal>
	)}
}

const mapStateToProps = state => {
    return {
        username: state.username,
    }
}


CreatePostModal.defaultProps = {
	isEdit: false,
	title: '',
	description: '',
	content: '',
	contentType: "text/plain",
	categories: [],
	visibility: 'PUBLIC',
	visibleTo: [],
	unlisted: false,
}

CreatePostModal.propTypes = {
	storeItems: PropTypes.object.isRequired,
	modalTrigger: PropTypes.object.isRequired,
	getPosts: PropTypes.func.isRequired,
	closeModal: PropTypes.func.isRequired,
}

export default connect(mapStateToProps)(CreatePostModal);