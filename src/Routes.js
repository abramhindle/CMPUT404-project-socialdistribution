import React from "react";
import { Route, Switch } from "react-router-dom";
import Home from "./components/pages/Home";
import Dashboard from "./components/pages/Inbox";
import Authors from "./components/pages/Authors";
import Author from "./components/pages/Author";



export default function Routes() {
  return (
    <Switch>
        <Route exact path='/dashboard' component={Dashboard}>
            <Dashboard/>
        </Route>
        <Route exact path='/service/authors' component={Authors}>
            <Authors/>
        </Route>
        <Route path='/service/author/:id' children={<Author/>} />
        <Route exact path="/">
            <Home />
        </Route>
    </Switch>
  );
}