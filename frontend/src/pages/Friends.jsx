import React, { Component } from 'react';
import {connect} from 'react-redux';
import * as FriendsActions from "../actions/FriendsActions";
import 'semantic-ui-css/semantic.min.css';
import FriendListComponent from '../components/FriendsListComponent';
import "./styles/Friends.css";
import { Button } from 'semantic-ui-react';
import store from "../store/index";

class Friends extends Component {

	constructor(props) {
		super(props);
		this.state = {
			userIdFullURL: null,
			isLoggedIn: false,
			usernameString: null,
			userId: null,
			listData: null,
			mode: "friends",
		}
	}
	
	componentDidMount(){
		let userIdString = ""
		try{
			userIdString = store.getState().loginReducers.userId.split("/")[4]
		}
		catch(e){
			console.log("Error: Could not retrieve user Id")
			return e
		}
		this.setState({
			userIdFullURL: store.getState().loginReducers.userId,
			userId: userIdString,
			isLoggedIn: store.getState().loginReducers.isLoggedIn,
			usernameString: store.getState().loginReducers.username,
		})
		let hostUrl = "/api/author/"+userIdString+""
		let requireAuth = true
		this.props.sendCurrentFriendsRequest(hostUrl,requireAuth)
		
		// Todo: Implement get request list
		hostUrl = "/api/followers/"+encodeURIComponent(store.getState().loginReducers.userId)
		this.props.sendPendingFriendsRequest(hostUrl,requireAuth)


	}

	GetListView = function(){
		if(this.state.mode === "friends"){
			return this.props.friends
		}
		else if (this.state.mode === "requests"){
			return this.props.requests
		}
		else{
			return null
		}
	}

	render() {
	return(	
		<div className="pusher">
			<h1>
				<div id="FriendDiv">
					<Button.Group id="ToggleFriendList">
						<Button id="friends" onClick={() =>{this.setState({mode: "friends"})}}>Current Friends</Button>
						<Button.Or />
						<Button id="requests" onClick={() =>{this.setState({mode: "requests"})}} color ="teal">Friend Requests</Button>
					</Button.Group>
					<FriendListComponent data={this.GetListView()}/>
				</div>
			</h1>
		</div>
	    )
    }
}
const mapDispatchToProps = dispatch => {
    return {
        sendCurrentFriendsRequest: (urlPath, requireAuth) => {
            return dispatch(FriendsActions.sendCurrentFriendsRequest(urlPath, requireAuth));
		},
		sendPendingFriendsRequest: (urlPath, requireAuth) => {
            return dispatch(FriendsActions.sendPendingFriendsRequest(urlPath, requireAuth));
        }
    }
}

const mapStateToProps = state => {
    return {
		friends: state.friendsReducers.friends,
		requests: state.friendsReducers.requests,
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(Friends);