import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router, Route, Redirect } from 'react-router-dom';

import ExpandPost from './containers/ExpandPost';
import Feed from './containers/Feed';
import Profile from './containers/Profile';
import Login from './containers/Login';
import Signup from './containers/Signup';
import ManageProfile from './containers/ManageProfile'

import { Provider } from 'react-redux';
import store from './store';

export default function App() {
    return (
        <Provider store={store}>
            <Router>
                <div 
                    className="app"
                >
                    <Route exact path="/">
                        <Redirect to="/login"/>
                    </Route>
                    <Route exact path="/author/:authorId/posts/:postId" component={ExpandPost}/>
                    <Route exact path="/post" component={ExpandPost}/>
                    <Route exact path="/feed" component={Feed}/>
                    <Route exact path="/profile" component={Profile}/>
                    <Route exact path="/manage-profile" component={ManageProfile}/>
                    <Route exact path="/login" component={Login}/>
                    <Route exact path="/signup" component={Signup}/>
                </div>
            </Router>
        </Provider>
    )
}

ReactDOM.render(<App />, document.getElementById('root'));