import React, { Component } from 'react';
import StreamFeed from '../components/StreamFeed';
import store from '../store/index.js';
import './styles/Stream.css';


class SinglePost extends Component {	

	render() {
		const urlPath = "/api/posts/" + this.props.match.params.postId
		const storeItems = store.getState().loginReducers;
		return(	
			<div className="pusher">
				<StreamFeed storeItems={storeItems} urlPath={urlPath} />
			</div>
			)
    }
}

export default SinglePost;
