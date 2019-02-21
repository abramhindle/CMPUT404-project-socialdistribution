import React, { Component } from 'react';
import { Feed } from 'semantic-ui-react';
import PostInput from '../components/PostInput';
import StreamPost from '../components/StreamPost';
import './styles/Stream.css';

class Stream extends Component {	

	constructor(props) {
		super(props);
		this.state = {
			events: []
		}
	};	

	createPostFromJson(payload){
		return(
						<StreamPost 
						key={payload.postID}
						username={payload.username} 
						profilePicture={payload.profilePicture}
						date={payload.date}
						content={payload.content}
						contentType={payload.contentType}
						/>
		)
	};

	componentDidMount() {
		// Request and get the posts
		var apiCallResults = [
						{
						postID: 1,
						username: "Henry",
						profilePicture: null,
						date: "4 days ago",
						content: "HELLO WORLD",
						contentType: "text/plain",
						},
						
						{
						postID: 2,
						username: "Henry2",
						profilePicture: null,
						date: "3 days ago",
						content: "AHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH",
						contentType: "text/plain",
						},
							
							
						{
						postID: 3,
						username: "Henry3",
						profilePicture: null,
						date: "4 days ago",
						content: "*THIS IS IN MARKDOWN*",
						contentType: "text/markdown",
						},
						
						{
						postID: 4,
						username: "Henry4",
						profilePicture: null,
						date: "4 days ago",
						content: "*EXPANDING THE*",
						contentType: "text/plain",
						},
						
						{
						postID: 5,
						username: "Henry5",
						profilePicture: null,
						date: "4 days ago",
						content: "FEED TO SHOW",
						contentType: "text/plain",
						},
						
						{
						postID: 6,
						username: "Henry6",
						profilePicture: null,
						date: "4 days ago",
						content: "A SCROLL BAR",
						contentType: "text/plain",
						},
						
						{
						postID: 7,
						username: "Henry7",
						profilePicture: null,
						date: "4 days ago",
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
	return(	
		<div className="pusher">
			<Feed>
				{this.state.events}
				<PostInput/>
			</Feed>
		</div>
	    )
    }
}

export default Stream;
