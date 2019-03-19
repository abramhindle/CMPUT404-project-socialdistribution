import React, { Component } from 'react';
import './App.css';
import Author from "./pages/Author";
import Stream from "./pages/Stream";
import SinglePost from "./pages/SinglePost";
import Login from "./pages/Login";
import Friends from "./pages/Friends";
import PublicStream from "./pages/PublicStream";
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
						<Route exact path="/author/:authorId" component={Author}/>
						<Route exact path ="/stream" component={Stream}/>
						<Route exact path="/posts/:postId" component={SinglePost}/>
						<Route exact path ="/friends" component={Friends}/>
						<Route exact path ="/public" component={PublicStream}/>
						<Route component={NotFound} />
					</Switch>
				</div>
			</BrowserRouter>
		);
  	}
}

export default App;