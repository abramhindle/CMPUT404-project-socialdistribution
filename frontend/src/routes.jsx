import React from 'react';
import {Route, Switch, Redirect} from 'react-router-dom';

/* Page Imports */
import LandingPage from './pages/landing';
import HomePage from './pages/homepage';
import NotFound from './pages/notfound';

/*
 * Central file for all routing related tasks.
 */
const BaseRouter = () => {
   return (
       <Switch>
            <Route exact path="/" component={LandingPage}/>
            <Route exact path="/Home" component={HomePage}/>
            <Route exact path="/NotFound" component={NotFound}/>
            <Redirect to="/NotFound"/> // If no route is found we automically default to NotFound
       </Switch>
   ); 
}

export default BaseRouter;
