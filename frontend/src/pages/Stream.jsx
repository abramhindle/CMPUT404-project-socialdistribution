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
<<<<<<< HEAD
				<StreamFeed storeItems={storeItems} urlPath="/api/author/posts/" />
=======
				<StreamFeed storeItems={storeItems} getGithub={true} urlPath="/api/author/posts/" />
>>>>>>> d9ab20f3e3189424f4baf8a3a973f1f5606201cc
                <SemanticToastContainer position="bottom-left"/>
			</div>
			)
    }
}

export default Stream;
