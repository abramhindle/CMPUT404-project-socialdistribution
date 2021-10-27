import React from "react";
import { Route, Switch } from "react-router-dom";
import Home from "./components/pages/Home";
import Login from "./components/pages/Login";



export default function Routes() {
  return (
    <Switch>
        <Route exact path="/login">
            <Login />
        </Route>
        <Route exact path="/">
            <Home />
        </Route>
    </Switch>
  );
}