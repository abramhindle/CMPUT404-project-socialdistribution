import React, { Component } from 'react';
import { Feed } from 'semantic-ui-react';
import CreatePostModal from '../components/CreatePostModal';
import StreamPost from '../components/StreamPost';
import store from '../store/index.js';
import './styles/Stream.css';

class Stream extends Component {	

	constructor(props) {
		super(props);
		this.state = {
			storeItems: [],
			events: [],
		}
	};	

	createPostFromJson(payload){
		return(
						<StreamPost 
						key={payload.postID}
						username={payload.username} 
						profilePicture={payload.profilePicture}
						date={payload.date}
						title={payload.title}
						description={payload.description}
						content={payload.content}
						contentType={payload.contentType}
						/>
		)
	};

	componentDidMount() {
		var apiCallResults = [
						{
						postID: 1,
						username: "Henry",
						profilePicture: null,
						date: "4 days ago",
						title: "TITLE",
						description: "DESCRIPTION",
						content: "HELLO WORLD",
						contentType: "text/plain",
						},
						
						{
						postID: 2,
						username: "Henry2",
						profilePicture: null,
						date: "3 days ago",
						title: "TITLE",
						description: "DESCRIPTION",
						content: "AHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH",
						contentType: "text/plain",
						},
							
							
						{
						postID: 3,
						username: "Henry3",
						profilePicture: null,
						date: "4 days ago",
						title: "TITLE",
						description: "DESCRIPTION",
						content: "*THIS IS IN MARKDOWN*",
						contentType: "text/markdown",
						},
						
						{
						postID: 4,
						username: "Henry4",
						profilePicture: null,
						date: "4 days ago",
						title: "TITLE",
						description: "DESCRIPTION",
						content: "*EXPANDING THE*",
						contentType: "text/plain",
						},
						
						{
						postID: 5,
						username: "Henry5",
						profilePicture: null,
						date: "4 days ago",
						title: "TITLE",
						description: "DESCRIPTION",
						content: "FEED TO SHOW",
						contentType: "text/plain",
						},
						
						{
						postID: 6,
						username: "Henry6",
						profilePicture: null,
						date: "4 days ago",
						title: "TITLE",
						description: "DESCRIPTION",
						content: "A SCROLL BAR",
						contentType: "text/plain",
						},
						
						{
						postID: 7,
						username: "Henry7",
						profilePicture: null,
						date: "4 days ago",
						title: "TITLE",
						description: "DESCRIPTION",
						content: "A buhhhhh",
						contentType: "text/plain",
						},	
										
						];
						
		var postList = [];
		apiCallResults.forEach(result => {
			postList.push(this.createPostFromJson(result));
		});
			
		this.setState({events: postList}, () =>{});
	}

	render() {
	const storeItems = store.getState().loginReducers;
	return(	
		<div className="pusher">
			<Feed>
				{this.state.events}
			</Feed>
			<div className="modalButtonPosition">
			<CreatePostModal storeItems={storeItems} />
			</div>
		</div>
	    )
    }
}

export default Stream;
