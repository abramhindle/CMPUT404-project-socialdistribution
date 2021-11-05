import React from "react";
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom'; 
import Home from "./pages/Home";
import Inbox from "./pages/Inbox";
import Stream from "./pages/Stream";
import Authors from "./pages/Authors";
import Author from "./pages/Author";
import NotFound from "./pages/NotFound";
import UserProvider from "./UserContext"
import "./App.css";

function App() {
  return (
    <UserProvider>
      <div className="App">
        <Router>
          <Switch>
              <Route exact path="/">
                  <Home />
              </Route>
              <Route exact path='/inbox' component={Inbox}>
                  <Inbox/>
              </Route>
              <Route exact path='/stream' component={Stream}>
                  <Stream/>
              </Route>
              <Route exact path='/service/authors' component={Authors}>
                  <Authors/>
              </Route>
              <Route path='/service/author/:id' component={Author} />
              <Route component={NotFound} />
          </Switch>
        </Router>
      </div>
    </UserProvider>
  );
}

export default App;
