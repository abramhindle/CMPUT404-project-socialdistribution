import React, { Component } from 'react';
import 'semantic-ui-css/semantic.min.css';
import { Sidebar, Menu, Icon } from 'semantic-ui-react';
import {Link} from "react-router-dom";
import './styles/SideBar.css';
import store from "../store/index";
import HTTPFetchUtil from "../util/HTTPFetchUtil";
import AbortController from 'abort-controller';
import Cookies from 'js-cookie';


const controller = new AbortController();
const signal = controller.signal;
signal.addEventListener("abort", () => {});

class SideBar extends Component {	

	constructor(props) {
		super(props);
		this.state = {
			haveFriendRequest: false,
			numFriendRequests: 0,
		};
	}
	
	componentDidMount() {
  		this.timer = setInterval(()=> this.checkForFriendRequest(), 5000);
	}

	componentWillUnmount() {
  		this.timer = null; 
	}
	
	checkForFriendRequest() {
		const fullAuthorId = store.getState().loginReducers.userId || Cookies.get("userID");
		const urlPath = "/api/followers/" + encodeURIComponent(fullAuthorId),
			requireAuth = true;
        HTTPFetchUtil.getRequest(urlPath, requireAuth, signal)
            .then((httpResponse) => {
                if (httpResponse.status === 200) {
                    httpResponse.json().then((results) => {
                    	if (results.authors.length > 0) {
							clearInterval(this.timer);
							this.timer = null;
							this.setState({
								haveFriendRequest: true,
								numFriendRequests: results.authors.length,
							});
    					}
                    })
                }
                else{
                    return httpResponse;
                }
            })
            .catch((error) => {
                console.error(error);
        });
	}

	render() {
		const userId = store.getState().loginReducers.userId || Cookies.get("userID");
		const displayName = store.getState().loginReducers.displayName || Cookies.get("displayName");
		const currentLocation = window.location.pathname.split('/')[1];
		
		let $friendRequestNotification = (<span></span>);
		if(this.state.haveFriendRequest && window.location.pathname !== "/friends") {
			$friendRequestNotification = (
					<span className="notificationNumber">{this.state.numFriendRequests} </span>
			);
		}
		
		if(window.location.pathname !== "/") {
			return(
					<Sidebar as={Menu} direction="left" width="thin" visible={true} inverted vertical icon color={"blue"} className="sideBarMenu">						
						
						<Menu.Item as={Link} to={"/author/" + encodeURIComponent(userId)} active={currentLocation === "author"} className="sideBarProfile">					
							<span className={"ui circular tiny bordered centered image"}> 	
								<img className="profileBubbleInSidebar" alt="It's you!" src={require('../assets/images/default2.png')}/>
								<span className="profileBubbleLetter"> {displayName.charAt(0).toUpperCase()} </span>
							</span>
							<figcaption>Profile</figcaption>
						</Menu.Item>

						<Menu.Item as={Link} to={"/stream"} active={currentLocation === "stream"} className="sideBarItem">
							<Icon name="tint"/>
						  	Stream
						</Menu.Item>

						<Menu.Item as={Link} to={"/friends"} active={currentLocation === "friends"} className="sideBarItem">
							{$friendRequestNotification}
							<Icon name="users"/>
						 	 Friends
						</Menu.Item>
						
						
						<Menu.Item as={Link} to={"/public"} active={currentLocation === "public"} className="sideBarItem">
							<Icon name="globe"/>
						  	Public
						</Menu.Item>

						<Menu.Item as={Link} to={"/logout"} className="sideBarItem">
							<Icon name="sign-out"/>
						  	Logout
						</Menu.Item>
						
					</Sidebar>
			)
		}
		else {
			return (<div>{null}</div>)
		}
	}
}

export default SideBar;