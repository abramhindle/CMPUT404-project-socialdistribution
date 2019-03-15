import React, { Component } from 'react';
import { Feed, Modal, Label } from 'semantic-ui-react';
import ReactMarkdown from 'react-markdown';
import ProfileBubble from './ProfileBubble';
import AnimatedButton from './AnimatedButton';
import CreatePostModal from '../components/CreatePostModal';

import store from '../store/index.js';
import PropTypes from 'prop-types';
import TextTruncate from 'react-text-truncate'; 
import './styles/StreamPost.css';

function categoryToLabel(category) {
	return (<Label key={category} tag> {category} </Label>);
}

class StreamPost extends Component {	

	constructor(props) {
		super(props);
		this.state = {
			showContentModal: false,
			showDeleteModal: false,
			showEditModal: false,
			yourOwnPost: false,
		}
		
		this.openContentModal = this.openContentModal.bind(this);
		this.closeContentModal = this.closeContentModal.bind(this);
		
		this.openDeleteModal = this.openDeleteModal.bind(this);
		this.closeDeleteModal = this.closeDeleteModal.bind(this);
		
		this.openEditModal = this.openEditModal.bind(this);
		this.closeEditModal = this.closeEditModal.bind(this);
		
		this.contentRender = this.contentRender.bind(this);
		this.deletePost = this.deletePost.bind(this);
		
		this.categoryLabels = this.categoryLabels.bind(this);
	}	
	
	componentDidMount() {
		if (this.props.author === this.props.viewingUser) {
			this.setState({
				yourOwnPost: true,
			});
		}
	}

	openContentModal(event) {
		if (!this.state.showEditModal && !this.state.showDeleteModal) {
			event.stopPropagation();
			this.setState({
				showContentModal: true,
			});
		}
	}
	
	closeContentModal() {
		this.setState({
			showContentModal: false,
		});
	}

	openDeleteModal(event) {
		event.stopPropagation();
		this.setState({
			showDeleteModal: true,
		});
	}
	
	closeDeleteModal() {
		this.setState({
			showDeleteModal: false,
		});
	}

	openEditModal(event) {
		event.stopPropagation();
		this.setState({
			showEditModal: true,
		});
	}
	
	
 	closeEditModal() {
 		this.setState({ 
 			showEditModal: false, 
 		});
	}


	contentRender(content, contentType) {
		switch(contentType) {
			case 'text/plain':
				return content; 
			case 'text/markdown':
				return <ReactMarkdown source={content}/>;
			case 'image/png;base64':
				return <img src={content} alt={content} />;
			case 'image/jpeg;base64':
				return <img src={content} alt={content}/>;
			default:
				return "Bad contentType. Can't display post";
		}
	}
	
	categoryLabels() {
		let labels = this.props.categories.map(categoryToLabel);
		return(
			<div className="categoryLabels">
			{labels}
			</div>
		);
	}
	
	deletePost(){
		this.closeDeleteModal();
		this.props.deletePost(this.props.index, this.props.postID);
	}
	
	render() {
		const storeItems = store.getState().loginReducers;
		let $modalTrigger = (<div><AnimatedButton 
				iconForButton={"pencil icon"} 
				buttonText={"EDIT"} 
				clickFunction={this.openEditModal}/></div>);
		return(
			<Feed.Event>
				<Feed.Label>
					<span className="profileBubbleInPost">
					<ProfileBubble username={this.props.displayName} profilePicture={this.props.profilePicture} profileBubbleClassAttributes={"ui circular bordered massive image"} />
					</span>
				</Feed.Label>
				<div className="postContent" onClick={this.openContentModal}>
				<Feed.Content>
					<div>
						<Feed.Summary>
							<span className="title"> <h3> 	<TextTruncate line={1} 
																text={this.props.title} 
																truncateText="..."
															/>
													</h3>
							</span>
							<div className="byAuthor"> by: {this.props.displayName} </div>
							
							<section className="description"> 
							{this.props.description} 
							</section>
						</Feed.Summary> 
					
					{this.state.yourOwnPost &&
					<Feed.Extra className="managePostButtons">
					
						<CreatePostModal 
							modalTrigger={$modalTrigger}
							isEdit={true}
							showModal={this.state.showEditModal}
							closeModal={this.closeEditModal}
							storeItems={storeItems} 
							
							postID={this.props.postID}
							title={this.props.title}
							description={this.props.description}
							content={this.props.content}
							contentType={this.props.contentType}
							categories={this.props.categories}
							visibility={this.props.visibility}
							visibleTo={this.props.visibleTo}
							unlisted={this.props.unlisted}
							
							getPosts={this.props.getPosts}
						/>
						
						<div><AnimatedButton iconForButton={"trash icon"} buttonText={"DELETE"} clickFunction={this.openDeleteModal}/></div>
					</Feed.Extra>
					}	
					
					<Feed.Date className="datetimeOfPost">
						{this.props.date}
					</Feed.Date>
					</div>
					
					
					<Modal 
					open={this.state.showContentModal}
					onClose={this.closeContentModal}
 					className={"contentPostModal"}
 					>
					<Modal.Header className='modalHeader'> {this.props.title} </Modal.Header>
					<Modal.Content>
						
					<section  className='contentModalContent'>
						{this.contentRender(this.props.content, this.props.contentType)}
					</section>
					
					</Modal.Content>
					{this.categoryLabels()}
					</Modal>
					
					
					<Modal
					open={this.state.showDeleteModal}
					onClose={this.closeDeleteModal}
					basic
					>
					<Modal.Header> DELETE THIS POST? </Modal.Header>
					
					<Modal.Content className='contentModalContent'>	
						<section>
							{this.contentRender(this.props.content, this.props.contentType)}
						</section>
					</Modal.Content>
					<Modal.Actions className="deletePostModalButtons">
						<AnimatedButton iconForButton={"cancel icon"} buttonText={"CANCEL"} clickFunction={this.closeDeleteModal}/>
						<AnimatedButton iconForButton={"trash icon"} buttonText={"DELETE"} clickFunction={this.deletePost}/>
					</Modal.Actions>
					</Modal>
					
				</Feed.Content>
				</div>
			</Feed.Event>
		)
	}
}

StreamPost.propTypes = {
	postID: PropTypes.string.isRequired,
	displayName: PropTypes.string.isRequired,
	profilePicture: PropTypes.string,
	title: PropTypes.string.isRequired,
	description: PropTypes.string.isRequired,
	content: PropTypes.string.isRequired,
	contentType: PropTypes.string.isRequired,
};

export default StreamPost;