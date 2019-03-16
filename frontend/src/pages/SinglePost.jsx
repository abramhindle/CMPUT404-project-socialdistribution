import React, { Component } from 'react';
import StreamFeed from '../components/StreamFeed';
import store from '../store/index.js';
import './styles/Stream.css';

//TODO: Change the urlPath to be the one for the logged in user.

class SinglePost extends Component {	

	render() {
		const urlPath = "/api/posts/" + this.props.match.params.postId
		const storeItems = store.getState().loginReducers;
		return(	
			<div className="pusher">
				<StreamFeed userID={storeItems.userId} urlPath={urlPath} />
			</div>
			)
    }
}

export default SinglePost;
