import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router, Route, Redirect } from 'react-router-dom';

import ExpandPost from './containers/ExpandPost';
import Feed from './containers/Feed';
import Profile from './containers/Profile';
import Login from './containers/Login';
import Signup from './containers/Signup';

export default function App() {
    return (
        <Router>
            <div 
                className="app"
            >
                <Route exact path="/">
                    <Redirect to="/feed"/>
                </Route>
                <Route exact path="/author/:authorId/posts/:postId" component={ExpandPost}/>
                <Route exact path="/feed" component={Feed}/>
                <Route exact path="/profile" component={Profile}/>
                <Route exact path="/login" component={Login}/>
                <Route exact path="/signup" component={Signup}/>
            </div>
        </Router>
    )
}

ReactDOM.render(<App />, document.getElementById('root'));