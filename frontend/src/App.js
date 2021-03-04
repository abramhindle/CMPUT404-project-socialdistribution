import React from "react";
import { BrowserRouter as Router, Route } from "react-router-dom";
import "./App.css";
import Home from "./components/Home";

export default class App extends React.Component {
  render() {
    return (
      <Router>
        {/* add route */}
        <Route exact path="/" component={Home} />
      </Router>
    );
  }
}
