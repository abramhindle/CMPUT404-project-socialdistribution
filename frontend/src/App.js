import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router, Route, Redirect } from 'react-router-dom';
import { Provider as AlertProvider } from 'react-alert';
import AlertTemplate from 'react-alert-template-basic';
import Alerts from './components/Alerts/Alerts';

import ExpandPost from './containers/ExpandPost';
import Feed from './containers/Feed';
import Profile from './containers/Profile';
import Login from './containers/Login';
import Signup from './containers/Signup';
import ManageProfile from './containers/ManageProfile'

import { Provider } from 'react-redux';
import store from './store';
import { Fragment } from 'react';

// Alert Options
const alertOptions = {
    timeout: 3000,
    position: 'top center'
}

export default function App() {
    return (
        <Provider store={store}>
            <AlertProvider template={AlertTemplate} {...alertOptions}>
                <Fragment>
                    <Alerts />
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
                </Fragment>
            </AlertProvider>
        </Provider>
    )
}

ReactDOM.render(<App />, document.getElementById('root'));