import React, { Component } from 'react';
import './App.css';
import Author from "./pages/Author";
import Stream from "./pages/Stream";
import SinglePost from "./pages/SinglePost";
import Login from "./pages/Login";
import Friends from "./pages/Friends";
import PublicStream from "./pages/PublicStream";
import NotFound from "./components/NotFound";
import {Route, Switch, BrowserRouter} from "react-router-dom";
import withAuth from "./components/HigherOrder/withAuth";
import Logout from "./pages/Logout";

class App extends Component {

	render() {
		return (
			<BrowserRouter>
				<Switch>
					<Route exact path="/" component={Login}/>
					<Route exact path="/author/:authorId" component={withAuth(Author)}/>
					<Route exact path ="/stream" component={withAuth(Stream)}/>
					<Route exact path="/posts/:postId" component={withAuth(SinglePost)}/>
					<Route exact path ="/friends" component={withAuth(Friends)}/>
					<Route exact path ="/public" component={withAuth(PublicStream)}/>
					<Route exact path ="/logout" component={Logout}/>
					<Route component={NotFound} />
				</Switch>
			</BrowserRouter>
		);
  	}
}

export default App;