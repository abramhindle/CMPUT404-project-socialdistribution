import React, { Component} from 'react';
import { Button, Icon, Feed, Loader } from 'semantic-ui-react';
import StreamPost from '../components/StreamPost';
import HTTPFetchUtil from '../util/HTTPFetchUtil.js';
import AbortController from 'abort-controller';
import PropTypes from 'prop-types';
import CreatePostModal from '../components/CreatePostModal';
import { toast } from 'react-semantic-toasts';
import 'react-semantic-toasts/styles/react-semantic-alert.css';
import './styles/StreamFeed.css';

const controller = new AbortController();
const signal = controller.signal;
signal.addEventListener("abort", () => {});

class StreamFeed extends Component {
	constructor(props) {
		super(props);
		this.state = {
			events: [],
			isFetching: false,
			showModal: false,
		};
		this.getPosts = this.getPosts.bind(this);
		this.closeModal = this.closeModal.bind(this);
		this.createPostFromJson = this.createPostFromJson.bind(this);
		this.deletePost = this.deletePost.bind(this);
	};	

 	closeModal() {
 		this.setState({ showModal: false});
	}

	createPostFromJson(payload){
		return(
			<StreamPost 
			key={payload.id}
			
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
			
			origin={payload.origin}
			
			author={payload.author.id}
			viewingUser={this.props.storeItems.userID}
			
			deletePost={this.deletePost}
			getPosts={this.getPosts}
			/>
		)
	};
	
	componentDidMount() {
		this.getPosts();							
	}

	componentWillUnmount() {
		controller.abort();
	}

	getPosts() {
		this.setState({
			isFetching: true,
		});

		const requireAuth = true, urlPath = this.props.urlPath;
			HTTPFetchUtil.getRequest(urlPath, requireAuth, signal)
			.then((httpResponse) => {
				if(httpResponse.status === 200) {
					httpResponse.json().then((results) => {	
						var postList = [];
						results.posts.forEach(result => {
							postList.push(this.createPostFromJson(result));
						});
						
						this.setState({
							events: postList,
							isFetching: false,
						});
					})
				}
				else {
					toast(
						{
							type: 'error',
							icon: 'window close',
							title: 'Failed',
							description: <p> Failed to retrieve posts. </p>,
						}
					);
					this.setState({
						isFetching: false,
					});
				}
			})
			.catch((error) => {
				console.error(error, "ERROR");

			});
	}
	
	deletePost(index, postID) {
		const requireAuth = true, urlPath = '/api/posts/' + postID;
			HTTPFetchUtil.deleteRequest(urlPath, requireAuth, signal)
			.then((httpResponse) => {
				if(httpResponse.status === 200) {	
					this.getPosts();
				}
				else {
					toast(
						{
							type: 'error',
							icon: 'window close',
							title: 'Failed',
							description: <p> Failed to delete post. </p>,
						}
					);
				}
			})
			.catch((error) => {
				console.error(error, "ERROR");
			});
	}
	
	render() {
		let $modalTrigger = (<Button fluid icon onClick={() => 
							this.setState({showModal: true})}> 
							<Icon name="send"/> Create Post 
							</Button>);
		return(	
		<div>
			<Feed>
				<Loader active={this.state.isFetching}/>
				{this.state.events}
			</Feed>
			<div className="modalButtonPosition">
				{this.props.displayCreatePostButton && 
				<CreatePostModal 
				modalTrigger={$modalTrigger}
				
				isEdit={false}
				showModal={this.state.showModal}
				closeModal={this.closeModal}
				storeItems={this.props.storeItems} 
				getPosts={this.getPosts}
				/>
				}
			</div>
		</div>
		)
    }
}

StreamFeed.defaultProps = {
	displayCreatePostButton: true,
}

StreamFeed.propTypes = {
	urlPath: PropTypes.string.isRequired,
	storeItems: PropTypes.object.isRequired,
}

export default StreamFeed;