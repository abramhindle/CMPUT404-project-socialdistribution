import React, { Component } from 'react';
import './App.css';
import Profile from "./pages/Profile";
import Stream from "./pages/Stream";
import Login from "./pages/Login";
import Friends from "./pages/Friends";
import Public from "./pages/Public";
import NotFound from "./components/NotFound";
import SideBar from "./components/SideBar";
import {Route, Switch, BrowserRouter} from "react-router-dom";

class App extends Component {

	render() {
		return (
			<BrowserRouter>
				<div>
					<SideBar/>
					<Switch>
						<Route exact path="/" component={Login}/>
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