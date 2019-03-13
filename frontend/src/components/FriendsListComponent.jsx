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
		let ListData = null;
		if(this.props["data"] != null){
			ListData = this.props["data"]
		}
		else{
			ListData = [{}]
		}
		
		return(
			<div>
				<List id="FriendList">
						{ListData.map(function(d, idx){
							return(
							<List.Item className="ListItem" key={idx}>
								<List.Content>
									<List.Header>{d.displayName}</List.Header>
									<List.Description>{d.host}</List.Description>
								</List.Content>
							</List.Item>
						)})}
				</List>
			</div>
		)
	}
}


export default (FriendListComponent);