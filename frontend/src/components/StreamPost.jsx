import React, { Component } from 'react';
import { Feed, Modal } from 'semantic-ui-react';
import ReactMarkdown from 'react-markdown';
import ProfileBubble from './ProfileBubble';
import AnimatedButton from './AnimatedButton';
import PropTypes from 'prop-types';
import './styles/StreamPost.css';

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
		
		this.contentRender = this.contentRender.bind(this);
		this.deletePost = this.deletePost.bind(this);
	}	
	
	componentDidMount() {
		if (this.props.author === this.props.viewingUser) {
			this.setState({
				yourOwnPost: true,
			});
		}
	}

	openContentModal() {
		this.setState({
			showContentModal: true,
		});
	}
	
	closeContentModal() {
		this.setState({
			showContentModal: false,
		});
	}

	openDeleteModal(event) {
		event.stopPropagation();
		event.nativeEvent.stopImmediatePropagation();
		this.setState({
			showDeleteModal: true,
		});
	}
	
	closeDeleteModal() {
		this.setState({
			showDeleteModal: false,
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
	
	deletePost(){
		this.closeDeleteModal();
		this.props.deletePost(this.props.index, this.props.postID);
	}
	
	render() {
	
		return(
			<Feed.Event>
				<Feed.Label>
					<span className="profileBubbleInPost">
					<ProfileBubble username={this.props.username} profilePicture={this.props.profilePicture} profileBubbleClassAttributes={"ui circular bordered massive image"} />
					</span>
					<figcaption className="profileBubbleName">{this.props.username}</figcaption>
				</Feed.Label>
				<Feed.Content>
					<div onClick={this.openModal}>
					<Feed.Summary>
						<span className="title"> <h3>{this.props.title} </h3></span>
						<section> {this.props.description} </section>
					</Feed.Summary> 
					
					{this.state.yourOwnPost &&
					<Feed.Extra className="managePostButtons">
					<div><AnimatedButton iconForButton={"pencil icon"} buttonText={"EDIT"} /></div>
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
					<Modal.Content className='contentModalContent'>
						
					<section>
						{this.contentRender(this.props.content, this.props.contentType)}
					</section>
					
					</Modal.Content>
					</Modal>
					
					
					<Modal
					open={this.state.showDeleteModal}
					onClose={this.closeDeleteModal}
					className={"deletePostModal"}
					>
					<Modal.Header className='modalHeader'> DELETE POST </Modal.Header>
					
					<Modal.Content className='contentModalContent'>	
						<section>
							{this.contentRender(this.props.content, this.props.contentType)}
						</section>
					</Modal.Content>
					<Modal.Actions>
						<AnimatedButton iconForButton={"trash icon"} buttonText={"DELETE"} clickFunction={this.deletePost}/>
					</Modal.Actions>
					</Modal>
					
				</Feed.Content>
			</Feed.Event>
		)
	}
}

StreamPost.propTypes = {
	postID: PropTypes.string.isRequired,
	username: PropTypes.string.isRequired,
	profilePicture: PropTypes.string,
	title: PropTypes.string.isRequired,
	description: PropTypes.string.isRequired,
	content: PropTypes.string.isRequired,
	contentType: PropTypes.string.isRequired,
};

export default StreamPost;