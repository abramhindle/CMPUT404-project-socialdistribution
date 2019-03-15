import React, { Component} from 'react';
import { Feed } from 'semantic-ui-react';
import StreamPost from '../components/StreamPost';
import HTTPFetchUtil from '../util/HTTPFetchUtil.js';
import PropTypes from 'prop-types';

class StreamFeed extends Component {
	constructor(props) {
		super(props);
		this.state = {
			posts: [],
			events: [],
		};
		this.getPosts = this.getPosts.bind(this);
		this.createPostFromJson = this.createPostFromJson.bind(this);
		this.deletePost = this.deletePost.bind(this);
	};	

	createPostFromJson(key, payload){
		return(
			<StreamPost 
			key={key}
			index={key}
			
			postID={payload.id}
			displayName={payload.author.displayName} 
			profilePicture={null}
			date={payload.published}
			title={payload.title}
			description={payload.description}
			content={payload.content}
			contentType={payload.contentType}
			categories={payload.categories}
			visibility={payload.visibility}
			visibleTo={payload.visibleTo}
			unlisted={payload.unlisted}
			
			author={payload.author.id}
			viewingUser={this.props.userID}
			
			deletePost={this.deletePost}
			getPosts={this.getPosts}
			/>
		)
	};
	
	componentDidMount() {
		this.getPosts();							
	}

	getPosts() {
		const requireAuth = true, urlPath = this.props.urlPath;
			HTTPFetchUtil.getRequest(urlPath, requireAuth)
			.then((httpResponse) => {
				if(httpResponse.status === 200) {
					httpResponse.json().then((results) => {	
						this.setState({
							posts: results.posts,
						});
						var postList = [];
						var key = 0;
						this.state.posts.forEach(result => {
							postList.push(this.createPostFromJson(key, result));
							key += 1;
						});
						
						this.setState({events: postList});
					})
				}
				else {
					alert("Failed to fetch posts");
				}
			})
			.catch((error) => {
				console.error(error, "ERROR");
			});
	}
	
	deletePost(index, postID) {
		const requireAuth = true, urlPath = '/api/posts/' + postID;
			HTTPFetchUtil.deleteRequest(urlPath, requireAuth)
			.then((httpResponse) => {
				if(httpResponse.status === 200) {	
					this.getPosts();
				}
				else {
					alert("Failed to delete post.");
				}
			})
			.catch((error) => {
				console.error(error, "ERROR");
			});
	}
	
	render() {
		return(	
			<Feed>
				{this.state.events}
			</Feed>
		)
    }
}

StreamFeed.propTypes = {
	urlPath: PropTypes.string,
	userID: PropTypes.string,
}

export default StreamFeed;