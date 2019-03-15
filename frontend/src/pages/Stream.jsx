import React, { Component } from 'react';
import { Button, Icon,} from 'semantic-ui-react';
import StreamFeed from '../components/StreamFeed';
import CreatePostModal from '../components/CreatePostModal';
import store from '../store/index.js';
import './styles/Stream.css';

//TODO: Change the urlPath to be the one for the logged in user.

class Stream extends Component {	

	constructor(props) {
		super(props);
		this.state = {
			showModal: false,
		};

		this.closeModal = this.closeModal.bind(this);
	}	

 	closeModal() {
 		this.setState({ showModal: false});
	}
	
	render() {
		const storeItems = store.getState().loginReducers;
		let $modalTrigger = (<Button fluid icon onClick={() => 
								this.setState({showModal: true})}> 
								<Icon name="send"/> Create Post 
								</Button>);
		return(	
			<div className="pusher">
				<StreamFeed userID={storeItems.userId} urlPath="/api/posts/" />
				<div className="modalButtonPosition">
					<CreatePostModal 
					modalTrigger={$modalTrigger}
					
					isEdit={false}
					showModal={this.state.showModal}
					closeModal={this.closeModal}
					storeItems={storeItems} 
					/>
				</div>
			</div>
			)
    }
}

export default Stream;
