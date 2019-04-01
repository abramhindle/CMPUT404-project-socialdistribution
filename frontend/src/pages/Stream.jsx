import React, { Component } from 'react';
import StreamFeed from '../components/StreamFeed';
import { SemanticToastContainer } from 'react-semantic-toasts';
import store from '../store/index.js';
import './styles/Stream.css';

class Stream extends Component {
	render() {
		const storeItems = store.getState().loginReducers;
		return(	
			<div className="pusher">
				<StreamFeed storeItems={storeItems} getGithub={true} urlPath="/api/author/posts/" />
                <SemanticToastContainer position="bottom-left"/>
			</div>
			)
    }
}

export default Stream;
