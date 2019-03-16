import React, { Component } from 'react';
import 'semantic-ui-css/semantic.min.css';
import {Link} from "react-router-dom";
import './styles/SideBar.css';
import store from "../store/index";

class SideBar extends Component {	

	constructor(props) {
		super(props);
		this.state = {
		};
	}	

	GetAuthorIdString(){
		let authorIdString = "";
		try{
			authorIdString = "/author/"+store.getState().loginReducers.userId.split("/")[4];
		}
		catch(e){
			console.log("Error: Could not retrieve user Id in profile");
			return e
		}
		return authorIdString
	}

	render() {
		if(window.location.pathname !== "/") {
			return(
					<div className="ui left fixed vertical inverted sidebar labeled icon menu blue visible sideBarMenu">						
						<Link to={this.GetAuthorIdString()} className="item sideBarProfile">
							<span className={"ui circular tiny bordered centered image"}>						
								<img alt="It's you!" src={require('../assets/images/default.png')}/>
							</span>
						  	<figcaption>Profile</figcaption>
						</Link>

						<Link to={"/stream"} className="item sideBarItem">
							<i className="tint icon"/>
						  	Stream
						</Link>

						<Link to="/friends" className="item sideBarItem">
							<i className="users icon"/>
						 	 Friends
						</Link>

						<Link to="/public" className="item sideBarItem">
							<i className="globe icon"/>
						  	Public
						</Link>

						<Link to="/" className="item sideBarItem">
							<i className="sign-out icon"/>
						  	Logout
						</Link>
					</div>
			)
		}
		else {
			return (<div>{null}</div>)
		}
	}
}

export default SideBar;