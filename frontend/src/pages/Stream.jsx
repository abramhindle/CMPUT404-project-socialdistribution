import React, { Component } from 'react';
import StreamFeed from '../components/StreamFeed';
import CreatePostModal from '../components/CreatePostModal';
import store from '../store/index.js';
import './styles/Stream.css';

//TODO: Change the urlPath to be the one for the logged in user.

class Stream extends Component {	

	render() {
		const storeItems = store.getState().loginReducers;
		return(	
			<div className="pusher">
				<StreamFeed storeItems={storeItems} urlPath="/api/posts/" />
				<div className="modalButtonPosition">
					<CreatePostModal storeItems={storeItems} />
				</div>
			</div>
			)
    }
}

export default Stream;
