import React, { Component } from 'react';
import './App.css';
import Profile from "./pages/Profile";
import Stream from "./pages/Stream";
import Friends from "./pages/Friends";
import Public from "./pages/Public";
import NotFound from "./components/NotFound";
import SideBar from "./components/SideBar";
import {Route, Switch, BrowserRouter} from "react-router-dom";
import LoginPage from "./login/LoginPage";

class App extends Component {

	render() {
		return (
			<BrowserRouter>
				<div>
					<SideBar/>
					<Switch>
						<Route exact path="/" component={LoginPage}/>
						<Route exact path="/profile" component={Profile}/>
						<Route exact path ="/stream" component={Stream}/>
						<Route exact path ="/friends" component={Friends}/>
						<Route exact path ="/public" component={Public}/>
						<Route component={NotFound} />
					</Switch>
				</div>
			</BrowserRouter>
		);
  	}
}

export default App;