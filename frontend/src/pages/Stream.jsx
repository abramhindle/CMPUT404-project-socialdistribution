import React, { Component } from 'react';
import StreamFeed from '../components/StreamFeed';
import store from '../store/index.js';
import './styles/Stream.css';

class Stream extends Component {	
	
	render() {
		const storeItems = store.getState().loginReducers;
		return(	
			<div className="pusher">
				<h1 className="streamHeader"> Stream </h1>
				<StreamFeed storeItems={storeItems} urlPath="/api/author/posts/" />
			</div>
			)
    }
}

export default Stream;
