import React, { Component } from 'react';
import 'semantic-ui-css/semantic.min.css';
import { Sidebar, Menu, Icon} from 'semantic-ui-react';
import {Link} from "react-router-dom";
import './styles/SideBar.css';
import store from "../store/index";
import Cookies from 'js-cookie';

class SideBar extends Component {	

	constructor(props) {
		super(props);
		this.state = {
		};
	}

	render() {
		const userId = store.getState().loginReducers.userId || Cookies.get("userID");
		const displayName = store.getState().loginReducers.displayName || Cookies.get("displayName");
		const currentLocation = window.location.pathname.split('/')[1];
		
		if(window.location.pathname !== "/") {
			return(
					<Sidebar as={Menu} direction="left" width="thin" visible={true} inverted vertical icon color={"blue"} className="sideBarMenu">						
						
						<Menu.Item as={Link} to={"/author/" + encodeURIComponent(userId)} active={currentLocation === "author"} className="sideBarProfile">					
							<span className={"ui circular tiny bordered centered image"}> 	
								<img className="profileBubbleInSidebar" alt="It's you!" src={require('../assets/images/default2.png')}/>
								<span className="profileBubbleLetter"> {displayName.charAt(0)} </span>
							</span>
							<figcaption>Profile</figcaption>
						</Menu.Item>

						<Menu.Item as={Link} to={"/stream"} active={currentLocation === "stream"} className="sideBarItem">
							<Icon name="tint"/>
						  	Stream
						</Menu.Item>

						<Menu.Item as={Link} to={"/friends"} active={currentLocation === "friends"} className="sideBarItem">
							<Icon name="users"/>
						 	 Friends
						</Menu.Item>
						
						
						<Menu.Item as={Link} to={"/public"} active={currentLocation === "public"} className="sideBarItem">
							<Icon name="globe"/>
						  	Public
						</Menu.Item>

						<Menu.Item as={Link} to={"/"} className="sideBarItem">
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