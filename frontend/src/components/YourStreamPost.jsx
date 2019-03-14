import React, { Component } from 'react';
import { Feed, Modal } from 'semantic-ui-react';
import ReactMarkdown from 'react-markdown';
import ProfileBubble from './ProfileBubble';
import PropTypes from 'prop-types';
import './styles/YourStreamPost.css';

class YourStreamPost extends Component {	

	constructor(props) {
		super(props);
		this.state = {
			showModal: false,
		}
		
		this.openModal = this.openModal.bind(this);
		this.closeModal = this.closeModal.bind(this);
		this.contentRender = this.contentRender.bind(this);
	}	

	openModal() {
		this.setState({
			showModal: true,
		});
	}
	
	closeModal() {
		this.setState({
			showModal: false,
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
	
					<Feed.Date className="datetimeOfPost">
						{this.props.date}
					</Feed.Date>
					
					
					</div>
					
					<Modal 
					open={this.state.showModal}
					onClose={this.closeModal}
 					className={"contentPostModal"}
 					>
					<Modal.Header className='contentPostHeader'> <h3> {this.props.title} </h3> </Modal.Header>
					<Modal.Content className='contentModalContent'>
						
					<section>
						{this.contentRender(this.props.content, this.props.contentType)}
					</section>
					
					</Modal.Content>
					</Modal>
				</Feed.Content>
			</Feed.Event>
		)
	}
}

YourStreamPost.propTypes = {
	username: PropTypes.string,
	profilePicture: PropTypes.string,
	title: PropTypes.string,
	description: PropTypes.string,
	content: PropTypes.string,
	contentType: PropTypes.string,
};

export default YourStreamPost;