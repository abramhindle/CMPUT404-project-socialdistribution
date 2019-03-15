import React, { Component} from 'react';
import { Button, Icon,} from 'semantic-ui-react';
import StreamFeed from '../components/StreamFeed';
import CreatePostModal from '../components/CreatePostModal';
import store from '../store/index.js';

class PublicStream extends Component {	
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
		return(	
			<div className="pusher">
				<StreamFeed userID={storeItems.userId} urlPath="/api/posts/" />
				<div className="modalButtonPosition">
					<CreatePostModal 
					modalTrigger={<Button fluid icon onClick={() => 
								this.setState({showModal: true})}> 
								<Icon name="send"/> Create Post 
								</Button>}
					
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


export default PublicStream;