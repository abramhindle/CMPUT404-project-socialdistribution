import React from "react";
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom'; 
import Home from "./pages/Home";
import Inbox from "./pages/Inbox";
import Authors from "./pages/Authors";
import Author from "./pages/Author";
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
              <Route exact path='/service/authors' component={Authors}>
                  <Authors/>
              </Route>
              <Route path='/service/author/:id' children={<Author/>} />
          </Switch>
        </Router>
      </div>
    </UserProvider>
  );
}

export default App;



