import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router, Route, Redirect } from 'react-router-dom';

import ExpandPost from './containers/ExpandPost';
import Feed from './containers/Feed';
import Profile from './containers/Profile';

export default function App() {
    return (
        <Router>
            <div 
                className="app"
                style={{ backgroundColor: "#EFEFEF"}}
            >
                <Route exact path="/">
                    <Redirect to="/feed"/>
                </Route>
                <Route exact path="/post" component={ExpandPost}/>
                <Route exact path="/feed" component={Feed}/>
                <Route exact path="/profile" component={Profile}/>
            </div>
        </Router>
    )
}

ReactDOM.render(<App />, document.getElementById('root'));