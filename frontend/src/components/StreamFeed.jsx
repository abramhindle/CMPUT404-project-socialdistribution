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
			github: [],
		};
		this.getPosts = this.getPosts.bind(this);
		this.closeModal = this.closeModal.bind(this);
		this.createPostFromJson = this.createPostFromJson.bind(this);
		this.deletePost = this.deletePost.bind(this);
		// this.fetchProfile = this.fetchProfile.bind(this);
		this.getGithub = this.getGithub.bind(this);
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
			
			isGithub={payload.isGithub}
			/>
		)
	};
	
	componentDidMount() {
		if (this.props.githuburl) {
			console.log("GETHUB");
			this.getGithub();
		}
		else {
			console.log("NORMAL");
			this.getPosts();
		}
	}
	
	componentDidUpdate(prevProps){
        if(prevProps.githuburl !== this.props.githuburl){    
			if (this.props.githuburl) {
				this.getGithub();
			}
			else {
				//this.getPosts();
			}
		}
	}
	

	getGithub() {
		const gituser = this.props.githuburl.split('/').filter(el => el).pop();
		const gitUrl = "https://api.github.com/users/" + gituser + "/received_events/public";
		let myHeaders = new Headers();

		if (this.state.ETag !== '') {
 			myHeaders.append('If-Modified-Since', this.state.ETag)
		}
		
		var myInit = { 
			method: 'GET', 
			headers: myHeaders,
			mode: 'cors',
			cache: 'default' 
		};
						
	
		let gitRequest = new Request(gitUrl, myInit);
		fetch(gitRequest) 
				.then(response => {
						if (response.status === 200) {
								response.json().then((results) =>  {
										this.setState({
											ETag: response.headers.get("ETag")
										});
										console.log("ETag set: ", this.state.ETag);
										
										let eventarray = [];
										for (let i = 0; i < results.length; i++) {
												const type = results[i].type.split(/(?=[A-Z])/)
												type.pop();
									
												const event = {
														id: "G " + results[i].id, //to identify as github, append G
														profilePicture: null,
														published: results[i].created_at,
														title: results[i].type,
														description: results[i].actor.display_login + " did " + results[i].type + " at " + results[i].repo.name, //my console log
														content: "",
														contentType: "text/plain",
														categories: [],
														visibility: "PUBLIC",
														visibleTo: [],
														unlisted: false,
														author: {
															id: "G " + results[i].id, //to identify as github, append G
															displayName: results[i].actor.display_login,
														},
														
														origin: "https://github.com/",
														
														deletePost: null,
														getPosts: null,
														isGithub: true,
												};
												eventarray.push(event)
										}
										
										this.setState({
											github: eventarray
										});
										this.getPosts();
								})
						} else {
								console.log("If we get a 304 response, we gucci. Else if to handle it", response);
								//throw new Error('Something went wrong on Github api server!');
						}
				})
				.then(response => {
						console.debug(response);
				}).catch(error => {
						console.error(error);
				});
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
						
						
						if (this.props.githuburl && this.state.github){
							let sortArray = this.state.github.concat(results.posts);
							sortArray.sort(function(a, b) {
							return (a.published > b.published) ? -1 : ((a.published < b.published) ? 1 : 0);
							});
							
							
							sortArray.forEach(result => {
								postList.push(this.createPostFromJson(result));
							});
						}
						
						else {
							results.posts.forEach(result => {
								postList.push(this.createPostFromJson(result));
							});
						}
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
	githuburl: PropTypes.string,
}

export default StreamFeed;