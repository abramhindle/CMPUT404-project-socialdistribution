import React from "react";
import { Route, Switch } from "react-router-dom";
import Home from "./components/pages/Home";
import Dashboard from "./components/pages/Dashboard";



export default function Routes() {
  return (
    <Switch>
        <Route exact path='/dashboard' component={Dashboard}>
            <Dashboard/>
        </Route>
        <Route exact path="/">
            <Home />
        </Route>
    </Switch>
  );
}