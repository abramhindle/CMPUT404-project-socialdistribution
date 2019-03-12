import React, { Component} from 'react';
import { Feed } from 'semantic-ui-react';
import StreamPost from '../components/StreamPost';
import CreatePostModal from '../components/CreatePostModal';
import HTTPFetchUtil from '../util/HTTPFetchUtil.js';

class Public extends Component {	

	constructor(props) {
		super(props);
		this.state = {
			posts: [],
			events: [],
		};
		this.getPublicPosts = this.getPublicPosts.bind(this);
	};	

	createPostFromJson(payload){
		return(
						<StreamPost 
						key={payload.id}
						username={payload.author.displayName} 
						profilePicture={null}
						date={payload.published}
						title={payload.title}
						description={payload.description}
						content={payload.content}
						contentType={payload.contentType}
						/>
		)
	};

	componentDidMount() {
		this.getPublicPosts();							
	}


	getPublicPosts() {
		const requireAuth = true, urlPath = "/api/posts/";
			HTTPFetchUtil.getRequest(urlPath, requireAuth)
			.then((httpResponse) => {
				if(httpResponse.status === 200) {
					httpResponse.json().then((results) => {	
						this.setState({
							posts: results.posts,
						});
						var postList = [];
						this.state.posts.forEach(result => {
							postList.push(this.createPostFromJson(result));
						});
			
		this.setState({events: postList});
					})
				}
			})
			.catch((error) => {
				console.error(error, "ERROR");
			});
	}


	render() {
	return(	
		<div className="pusher">
			<Feed>
				{this.state.events}
			</Feed>
			<div className="modalButtonPosition">
			<CreatePostModal/>
			</div>
		</div>
	    )
    }
}


export default Public;