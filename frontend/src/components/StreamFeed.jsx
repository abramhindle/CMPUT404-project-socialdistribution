import React, { Component} from 'react';
import { Button, Icon, Feed, Loader } from 'semantic-ui-react';
import StreamPost from '../components/StreamPost';
import HTTPFetchUtil from '../util/HTTPFetchUtil.js';
import PropTypes from 'prop-types';
import CreatePostModal from '../components/CreatePostModal';
import { toast } from 'react-semantic-toasts';
import 'react-semantic-toasts/styles/react-semantic-alert.css';
import './styles/StreamFeed.css';


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
			this.getGithub();
		}
		else {
			this.getPosts();
		}
	}

	getGithub() {
		const gituser = this.props.githuburl.split('/').filter(el => el).pop();
		const gitUrl = "https://api.github.com/users/" + gituser + "/received_events/public";
		// let myHeaders = new Headers();
		// let githubinfo = {
		// 		postID: "",
		// 		displayName: "",
		// 		profilePicture: "",
		// 		date: "",
		// 		title: "",
		// 		description: "", //my console log
		// 		content: "",
		// 		contentType: "text/plain",
		// 		categories: [],
		// 		visibility: "PUBLIC",
		// 		visibleTo: [],
		// 		unlisted: false,
		// 		author: "", //github displayname
		// 		viewingUser: "", //logged in user via cookie/store
		// 		deletePost: null,
		// 		getPosts: null,
		// }
		// if (this.state.ETag !== '') {
		// 		myHeaders.append('If-None-Match', this.state.ETag)
		// }
		// const myInit = {headers: myHeaders};
		console.log(gitUrl);
		fetch(gitUrl) //add myinit later?
				.then(response => {
						if (response.status === 200) {
								response.json().then((results) =>  {
										console.log('len', results.length);
										// console.log('Etag', response.headers.get("ETag"));
										// this.setState({
										//     ETag: response.headers.get("ETag")
										// });
										let eventarray = []
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
														deletePost: null,
														getPosts: null,
														isGithub: true,
												};
												// console.log(event)
												eventarray.push(event)
												// console.log("Event:", results[i].id, gituser, "Date:", results[i].created_at, results[i].payload.action, 'a', type.join(), 'in', results[i].repo.name);
										}
										console.log("eventarray", eventarray)
										this.setState({
											github: eventarray
										});
										this.getPosts();
								})
						} else {
								throw new Error('Something went wrong on Github api server!');
						}
				})
				.then(response => {
						console.debug(response);
				}).catch(error => {
						console.error(error);
				});
	}

	getPosts() {
		this.setState({
			isFetching: true,
		});

		console.log("PROOPS: ", this.props)
		console.log('propgit', this.props.githuburl);

		const requireAuth = true, urlPath = this.props.urlPath;
			HTTPFetchUtil.getRequest(urlPath, requireAuth)
			.then((httpResponse) => {
				if(httpResponse.status === 200) {
					httpResponse.json().then((results) => {
						var postList = [];
						
						
						if (this.props.githuburl && this.state.github){
							let sortArray = this.state.github.concat(results.posts);
							sortArray.sort(function(a, b) {
							return (a.published > b.published) ? -1 : ((a.published < b.published) ? 1 : 0);
							});
							
							console.log("SSSS", sortArray);
							
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
			HTTPFetchUtil.deleteRequest(urlPath, requireAuth)
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