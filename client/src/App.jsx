import './App.css';
import React from 'react';
import { Route, BrowserRouter, Switch } from 'react-router-dom';
import Navbar from "./components/Navbar"
import Home from "./pages/Home"
import Login from "./pages/Login"
import Register from "./pages/Login"
import Friends from "./pages/Friends"
import MyPosts from "./pages/MyPosts"
import SubmitPost from "./pages/SubmitPost"

const App = () => (
  <BrowserRouter>
    <Navbar />
    <Switch>
      <Route path="/friends">
        <Friends />
      </Route>
      <Route path="/myposts">
        <MyPosts />
      </Route>
      <Route path="/submit">
        <SubmitPost />
      </Route>
      <Route path="/login">
        <Login />
      </Route>
      <Route path="/register">
        <Register />
      </Route>
      <Route path="/">
        <Home />
      </Route>
    </Switch>
  </BrowserRouter>
);

export default App;
