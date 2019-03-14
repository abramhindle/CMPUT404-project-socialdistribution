import React, { Component} from 'react';
import StreamFeed from '../components/StreamFeed';
import CreatePostModal from '../components/CreatePostModal';
import store from '../store/index.js';

class PublicStream extends Component {	
	render() {
		const storeItems = store.getState().loginReducers;
		return(	
			<div className="pusher">
				<StreamFeed storeItems={storeItems} urlPath="/api/posts/"/>
				<div className="modalButtonPosition">
					<CreatePostModal storeItems={storeItems} />
				</div>
			</div>
			)
	}
}


export default PublicStream;