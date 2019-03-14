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
		let authorIdString = "" 
		try{
			authorIdString = "/author/"+store.getState().loginReducers.userId.split("/")[4].replace(/-/g,'');
		}
		catch(e){
			console.log("Error: Could not retrieve user Id in profile")
			return e
		}
		console.log(authorIdString)
		return authorIdString
	}

	render() {
		if(window.location.pathname !== "/") {
			return(
					<div className="ui left fixed vertical inverted sidebar labeled icon menu blue visible sideBarMenu">						
						<Link to={this.GetAuthorIdString()} className="item sideBarProfile">
							<span className={"ui circular tiny bordered centered image"}>						
								<img alt={this.props.username} src={require('../assets/images/default.png')}/>
							</span>
						  	<figcaption>Profile</figcaption>
						</Link>

						<Link to={"/stream"} className="item sideBarItem">
							<i className="tint icon"></i>
						  	Stream
						</Link>

						<Link to="/friends" className="item sideBarItem">
							<i className="users icon"></i>
						 	 Friends
						</Link>

						<Link to="/public" className="item sideBarItem">
							<i className="globe icon"></i>
						  	Public
						</Link>

						<Link to="/" className="item sideBarItem">
							<i className="sign-out icon"></i>
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