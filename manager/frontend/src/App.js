import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router, Route, Redirect } from 'react-router-dom';

import Feed from './containers/Feed';

import Navbar from './components/Navbar/Navbar';

export default function App() {
    return (
        <Router>
            <div 
                className="app"
                style={{ backgroundColor: "#EFEFEF" }}
            >      
                <Navbar />
                <Route exact path="/">
                    <Redirect to="/feed"/>
                </Route>
                <Route exact path="/feed" component={Feed}/>
            </div>
        </Router>
    )
}

ReactDOM.render(<App />, document.getElementById('root'));