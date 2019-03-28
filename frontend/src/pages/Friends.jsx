import React, { Component } from 'react';
import {connect} from 'react-redux';
import * as FriendsActions from "../actions/FriendsActions";
import 'semantic-ui-css/semantic.min.css';
import FriendListComponent from '../components/FriendsListComponent';
import "./styles/Friends.css";
import { Button } from 'semantic-ui-react';
import store from "../store/index";
import HTTPFetchUtil from "../util/HTTPFetchUtil";
import AbortController from 'abort-controller';
import { SemanticToastContainer, toast } from 'react-semantic-toasts';
import 'react-semantic-toasts/styles/react-semantic-alert.css';
import Cookies from 'js-cookie';
import utils from "../util/utils";

const controller = new AbortController();
const signal = controller.signal;
signal.addEventListener("abort", () => {});

class Friends extends Component {

	constructor(props) {
		super(props);
		this.state = {
			userIdFullURL: null,
			isLoggedIn: false,
			userId: null,
			listData: null,
			mode: "friends",
			hostName: "",
			friendButtonColor: "teal",
			requestButtonColor: "grey",
		}
		this.removeFriend = this.removeFriend.bind(this);
		this.approveFriendRequest = this.approveFriendRequest.bind(this);
	}
	
	componentDidMount(){
		try{
			const userIdShortString = utils.getShortAuthorId(Cookies.get("userID")) || store.getState().loginReducers.authorId;
			const userIdString = Cookies.get("userID") || store.getState().loginReducers.userId;
			const hostNameString = utils.getHostName(Cookies.get("userID")) || store.getState().loginReducers.hostName;

			if(userIdShortString === null || userIdString === null || hostNameString === null){
				console.error("Error: Login credentials expired")
				return null
			}

			this.setState({
				userIdFullURL: userIdString,
				hostName: hostNameString,
				userId: userIdShortString,
				isLoggedIn: store.getState().loginReducers.isLoggedIn,
			})
			let hostUrl = "/api/author/"+userIdShortString+""
			const requireAuth = true
			this.props.getCurrentApprovedFriends(hostUrl,requireAuth)
			hostUrl = "/api/followers/"+userIdShortString
			this.props.getCurrentFriendsRequests(hostUrl,requireAuth)
		}
		catch(e){
			console.log(e);
			toast(
				{
					type: 'error',
					icon: 'warning',
					title: 'Error loading friends!'
				}
			);
		}
	}

	getListView = function(){
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

	getLocalDisplayName(){
		let displayName;
		if(Cookies.get("displayName") !== null){
            displayName = Cookies.get("displayName");
        }
        else if(store.getState().loginReducers.displayName !== "null"){
            displayName = store.getState().loginReducers.displayName;
        }
        else{
            displayName = null;
		}
		return displayName;
	}

	getLocalHost(){
		let host;
		if(Cookies.get("userID") !== null){
            host = Cookies.get("userID");
        }
        else if(store.getState().loginReducers.url !== "null"){
            host = store.getState().loginReducers.url;
        }
        else{
            host = null;
		}
		return host;
	}

	

	approveFriendRequest(authorObj){
		const displayName = this.getLocalDisplayName()
		const url = this.getLocalHost()
		const urlPath = "/api/friendrequest/"
		const body = {
			query: "friendrequest",
			author: {
				id: this.state.userIdFullURL,
				host: "http://"+this.state.hostName+"/",
				displayName: displayName,
				url: url,
			},
			friend:{
				id: authorObj.id,
				host: authorObj.host,
				displayName: authorObj.displayName,
				url: authorObj.id,
			}
		}
		HTTPFetchUtil.sendPostRequest(urlPath, true, body, signal)
            .then((httpResponse) => {
                if (httpResponse.status === 200) {
                    httpResponse.json().then((results) => { 
						this.updateRenderAccept()
						this.updateRenderRemove()
						toast(
							{
								type: 'success',
								icon: 'user',
								title: 'Request accepted!',
								description: <p>You are now friends with {authorObj.displayName}</p>
							}
						);

                    })
				}
				else{
					toast(
						{
							type: 'error',
							icon: 'warning',
							title: 'Error: Request could not be accepted!'
						}
					);
				}
            })
            .catch((error) => {
                console.error(error);
        });
	}

	updateRenderRemove(){
		const authorIdString = this.state.userId
		const hostUrl = "/api/author/"+authorIdString+""
		this.props.getCurrentApprovedFriends(hostUrl,true)
	}

	updateRenderAccept(){
		const authorIdString = this.state.userId
		const hostUrl = "/api/followers/"+authorIdString+""
		this.props.getCurrentFriendsRequests(hostUrl,true)
	}

	removeFriend(authorObj){
		const displayName = this.getLocalDisplayName()
		const url = this.getLocalHost()
		const urlPath = "/api/unfollow/"
		const body = {
			query: "unfollow",
			author: {
				id: this.state.userIdFullURL,
				host: "http://"+this.state.hostName+"/",
				displayName: displayName,
				url: url
				
			},
			friend:{
				id: authorObj.id,
				host: authorObj.host,
				displayName: authorObj.displayName,
				url: authorObj.id,

			}
		}
		HTTPFetchUtil.sendPostRequest(urlPath, true, body, signal)
            .then((httpResponse) => {
                if (httpResponse.status === 200) {
                    httpResponse.json().then((results) => { 
						try{
							this.updateRenderAccept()
							this.updateRenderRemove()
						}
						catch(error){
							toast(
								{
									type: 'error',
									icon: 'warning',
									title: 'Could not refresh feed!'
								}
							);
						}
						toast(
							{
								type: 'warning',
								icon: 'user',
								title: 'Friend removed!',
								description: <p>You are no longer friends with {authorObj.displayName}</p>
							}
						);

                    })
				}
				else{
					toast(
						{
							type: 'error',
							icon: 'warning',
							title: 'Error: Friend could not be removed!'
						}
					);
				}
            })
            .catch((error) => {
                console.error(error);
        });
	}

	render() {
	return(	
		<div className="pusher">
			<h1 className="friendsHeader"> Friends </h1>
			<div id="FriendDiv">
				<Button.Group id="ToggleFriendList">
					<Button id="friends" onClick={() =>{this.setState({mode: "friends",friendButtonColor: "teal", requestButtonColor: "grey"})}} color={this.state.friendButtonColor}>Current Friends</Button>
					<Button.Or/>
					<Button id="requests" onClick={() =>{this.setState({mode: "requests",friendButtonColor: "grey", requestButtonColor: "teal"})}} color ={this.state.requestButtonColor}>Friend Requests</Button>
				</Button.Group>
				<FriendListComponent data={this.getListView()} mode={this.state.mode} acceptRequest={this.approveFriendRequest} rejectRequest={this.removeFriend} viewOwnFriendlist={true}/>
				<SemanticToastContainer position="bottom-left"/>
			</div>
		</div>
	    )
    }
}
const mapDispatchToProps = dispatch => {
    return {
        getCurrentApprovedFriends: (urlPath, requireAuth) => {
            return dispatch(FriendsActions.getCurrentApprovedFriends(urlPath, requireAuth));
		},
		getCurrentFriendsRequests: (urlPath, requireAuth) => {
            return dispatch(FriendsActions.getCurrentFriendsRequests(urlPath, requireAuth));
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