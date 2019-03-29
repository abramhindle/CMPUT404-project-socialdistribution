import React, { Component } from 'react';
import 'semantic-ui-css/semantic.min.css';
import { Comment, Header, Form, Input, Button, Loader, Message} from 'semantic-ui-react';
import ProfileBubble from './ProfileBubble';
import Cookies from 'js-cookie';
import HTTPFetchUtil from "../util/HTTPFetchUtil";
import PropTypes from 'prop-types';
import './styles/CommentsOnPost.css';

class CommentsOnPost extends Component {	

	constructor(props) {
		super(props);
		this.state = {
			comments: [],
			commentText: '',
			isFetching: false,
			failedFetch: false,
		};
		this.createCommentList = this.createCommentList.bind(this);
		this.getComments = this.getComments.bind(this);
		this.handleChange = this.handleChange.bind(this);
		this.submitComment = this.submitComment.bind(this);
	}

	componentDidMount() {
		this.getComments();
	}

	getComments() {
		this.setState({
			isFetching: true,
		});
		const requireAuth = true;
		const urlPath = "/api/posts/" + this.props.postID;
			HTTPFetchUtil.getRequest(urlPath, requireAuth)
			.then((httpResponse) => {
				if(httpResponse.status === 200) {
					httpResponse.json().then((results) => {	
						var commentList = [];
						console.log("RRR", results);
						results.posts[0].comments.forEach(result => {
							commentList.push(result);
						});
						
						this.setState({
							comments: commentList,
							isFetching: false,
						});
					})
				}
				else {
					this.setState({
						isFetching: false,
						failedFetch: true,
					});
				}
			})
			.catch((error) => {
				console.error(error, "ERROR");
			});
	}

	handleChange(event) {
		this.setState({[event.target.name]: event.target.value});
	}
	
	
	submitComment() {
		const urlPath = "/api/posts/" + this.props.postID + "/comments";
		const requireAuth = true;
		const requestBody = {
			query: "addComment",
			post: this.props.postID,
			comment: {
				author: {
					id: Cookies.get("userID"),
				},
				comment: this.state.commentText,
				contentType: "text/plain",
			}
		}
		
		HTTPFetchUtil.sendPostRequest(urlPath, requireAuth, requestBody)
		    .then((httpResponse) => {
		        if (httpResponse.status === 200) {
					this.setState({
						commentText: '',
					});	
					this.getComments();						
		        }
		        else {
					alert("Failed to add comment");
		        }
		    })
		    .catch((error) => {
		        console.error(error);
			});		
	}
	
	createCommentList(comment) {
		const commentID = comment.id;
		const author = comment.author.displayName;
		const authorID = comment.author.id;
		const date = comment.published;
		const commentText = comment.comment;
		return (
			<span key={commentID} className="singleComment">
				<Comment>
					<span className="profileBubbleInComment">
						<ProfileBubble 
							displayName={author} 
							userID={authorID}
							profilePicture={null} 
							profileBubbleClassAttributes={"ui circular bordered mini image"} 
						/>
					</span>
					
					<Comment.Content>
						<Comment.Author> {author} </Comment.Author>
						<Comment.Metadata> {date} </Comment.Metadata>
						<Comment.Text> {commentText} </Comment.Text>
					</Comment.Content>
					
				</Comment>
			</span>
		);
	}


	render() {
		let $commentSection;
		if (this.state.failedFetch) {
			$commentSection = 	<Message negative>
									<Message.Header>Fetch comments failed</Message.Header>
								</Message>;
		}
		else {
			$commentSection = this.state.comments.map(this.createCommentList);
			if ($commentSection.length < 1) {
				$commentSection = <p> No comments yet...</p>;
			}
		}
	
		return (
			<span>
				<Comment.Group>
					<Header as='h3' dividing>
						Comments
					</Header>
					{this.state.isFetching && <Loader/>}
					{!this.state.isFetching && $commentSection}
				</Comment.Group>
				<Form>
					<Input 	
								name="commentText"
								action={<Button onClick={this.submitComment}> Submit </Button>}
								className="commentInputBox" 
								placeholder="Add a comment..."
								size="small"
								value={this.state.commentText}
								onChange={this.handleChange}
					/>
				</Form>
			</span>
		);
	}
}

CommentsOnPost.propTypes = {
	postID: PropTypes.string.isRequired,
}

export default CommentsOnPost;
