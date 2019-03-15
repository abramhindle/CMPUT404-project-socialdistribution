import React, { Component} from 'react';
import { Feed, Loader } from 'semantic-ui-react';
import StreamPost from '../components/StreamPost';
import HTTPFetchUtil from '../util/HTTPFetchUtil.js';
import PropTypes from 'prop-types';

class StreamFeed extends Component {
	constructor(props) {
		super(props);
		this.state = {
			events: [],
			isFetching: false,
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
		this.setState({
			isFetching: true,
		});

		const requireAuth = true, urlPath = this.props.urlPath;
			HTTPFetchUtil.getRequest(urlPath, requireAuth)
			.then((httpResponse) => {
				if(httpResponse.status === 200) {
					httpResponse.json().then((results) => {	
						var postList = [];
						var key = 0;
						results.posts.forEach(result => {
							postList.push(this.createPostFromJson(key, result));
							key += 1;
						});
						
						this.setState({
							events: postList,
							isFetching: false,
						});
					})
				}
				else {
					alert("Failed to fetch posts");
					this.setState({
						isFetching: false,
					});
				}
			})
			.catch((error) => {
				console.error(error, "ERROR");
				this.setState({
					isFetching: false,
				});
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
				<Loader active={this.state.isFetching}/>
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