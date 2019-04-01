import React, { Component} from 'react';
import StreamFeed from '../components/StreamFeed';
import { SemanticToastContainer } from 'react-semantic-toasts';
import store from '../store/index.js';
import './styles/PublicStream.css';

class PublicStream extends Component {	
	
	render() {
		const storeItems = store.getState().loginReducers;
		return(	
			<div className="pusher">
				<StreamFeed storeItems={storeItems} urlPath="/api/posts/" />
                <SemanticToastContainer position="bottom-left"/>
			</div>
			)
    }
}


export default PublicStream;