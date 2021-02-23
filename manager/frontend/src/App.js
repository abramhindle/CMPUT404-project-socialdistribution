import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router, Route, Redirect } from 'react-router-dom';

import ExpandPost from './containers/ExpandPost';
import Feed from './containers/Feed';
import Profile from './containers/Profile';
import Login from './containers/Login';

export default function App() {
    return (
        <Router>
            <div 
                className="app"
            >
                <Route exact path="/">
                    <Redirect to="/feed"/>
                </Route>
                <Route exact path="/post" component={ExpandPost}/>
                <Route exact path="/feed" component={Feed}/>
                <Route exact path="/profile" component={Profile}/>
                <Route exact path="/login" component={Login}/>
            </div>
        </Router>
    )
}

ReactDOM.render(<App />, document.getElementById('root'));