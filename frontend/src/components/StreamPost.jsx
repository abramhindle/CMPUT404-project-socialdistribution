import React, { Component } from 'react';
import { Feed } from 'semantic-ui-react';
import ReactMarkdown from 'react-markdown';
import ProfileBubble from './ProfileBubble';
import './styles/StreamPost.css';

class StreamPost extends Component {	

	constructor(props) {
		super(props);
		this.state = {
		}
		console.log(props);
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
					<Feed.Extra>
						<span className="title"> <h3>{this.props.title} </h3></span>
						<section> {this.props.description} </section>
					</Feed.Extra> 

					<Feed.Date className="datetimeOfPost">
						{this.props.date}
					</Feed.Date>
				</Feed.Content>
			</Feed.Event>
		)
	}
}

export default StreamPost;