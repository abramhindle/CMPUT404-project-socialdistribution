import React, { Component } from 'react';
import { List, Image } from 'semantic-ui-react';
import "./styles/FriendsListComponent.css";

class FriendListComponent extends Component {	

	constructor(props) {
		super(props);
		this.state = {
		}
	}	
    render() {
			const ListData = this.props["data"]
			return(
				<div>
					{console.log(ListData,"checkcheck")}
				</div>
			)
	}
}


export default (FriendListComponent);