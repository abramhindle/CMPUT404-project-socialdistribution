import React, { Component } from 'react';
import './App.css';
import Stream from "./pages/Stream";
import NotFound from "./components/NotFound";
import {Route, Switch, BrowserRouter} from "react-router-dom";
import LoginPage from "./login/LoginPage";

class App extends Component {
	render() {
		return (
			<BrowserRouter>
				<Switch>
					<Route exact path="/" component={LoginPage}/>
					<Route exact path ="/stream" component={Stream}/>
					<Route component={NotFound} />
				</Switch>
			</BrowserRouter>
		);
  	}
}

export default App;