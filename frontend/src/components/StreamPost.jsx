import React, { Component } from 'react';
import 'semantic-ui-css/semantic.min.css';
import ReactMarkdown from 'react-markdown';
import ProfileBubble from './ProfileBubble';
import './styles/StreamPost.css';

class StreamPost extends Component {	

	constructor(props) {
		super(props);
		this.state = {
		}
	}	

	render() {
		return(
			<div className="event">
				<div className="label">
					<ProfileBubble username={this.props.username} profilePicture={this.props.profilePicture}/>
					<figcaption>{this.props.username}</figcaption>
				</div>
				<div className="content">
				
					{ this.props.contentType==="text/plain"
					? <div className="extra text">
							<section> {this.props.content} </section>
						</div> 
					:<div></div>
					}
					
					{ this.props.contentType==="text/markdown"
					? <div className="extra text">
							<section> <ReactMarkdown source={this.props.content}/> </section>
						</div> 
					:<div></div>
					}
					
					<div className="date">
						{this.props.date}
					</div>
				</div>
				
			</div>
		)
		
	}
}

export default StreamPost;