import React from "react";
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom'; 
import "./App.css";
import Routes from "./Routes.js";

function App() {
  return (
    <div className="App">
      <Router>
        <Switch>
        </Switch>
      </Router>
    <Routes/>
    </div>
  );
}

export default App;



