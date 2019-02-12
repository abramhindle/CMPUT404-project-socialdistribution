import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import PonyNote from "./components/PonyNote";
import Stream from "./pages/Stream";
import NotFound from "./components/NotFound";
import {Route, Switch, BrowserRouter} from "react-router-dom";
import {createStore, applyMiddleware} from "redux";
import {Provider} from "react-redux";
import ponyApp from "./reducers";
import thunk from "redux-thunk";
import LoginPage from "./login/LoginPage";

// let store = createStore(ponyApp);

class App extends Component {
	render() {
    	return (
        // <Provider store={store}>
			<BrowserRouter>
				<Switch>
              {/* <Route exact path="/" component={Stream}/> */} 
					<Route exact path="/" component={LoginPage}/>
					<Route exact path ="/stream" component={Stream}/>
					<Route component={NotFound} />
				</Switch>
			</BrowserRouter>
        // </Provider>
    );
  }
}

export default App;