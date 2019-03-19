import React, { Component} from 'react';
import StreamFeed from '../components/StreamFeed';
import store from '../store/index.js';

class PublicStream extends Component {	
	
	render() {
		const storeItems = store.getState().loginReducers;
		return(	
			<div className="pusher">
				<StreamFeed storeItems={storeItems} urlPath="/api/posts/" />
			</div>
			)
    }
}


export default PublicStream;