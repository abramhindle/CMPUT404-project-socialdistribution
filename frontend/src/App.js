import React, { Component } from 'react';
import './App.css';
import Stream from "./pages/Stream";
import Login from "./pages/Login";
import NotFound from "./components/NotFound";
import {Route, Switch, BrowserRouter} from "react-router-dom";

class App extends Component {
	render() {
		return (
			<BrowserRouter>
				<Switch>
					<Route exact path="/" component={Login}/>
					<Route path="/stream" component={Stream}/>
					<Route component={NotFound} />
				</Switch>
			</BrowserRouter>
		);
  	}
}

export default App;