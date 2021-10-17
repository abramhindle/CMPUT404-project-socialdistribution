import './App.css';
import React, { useEffect, useState } from 'react';
import { Route, BrowserRouter, Switch } from 'react-router-dom';
import Navbar from "./components/Navbar"
import Home from "./pages/Home"
import Login from "./pages/Login"
import Register from "./pages/Register"
import Friends from "./pages/Friends"
import MyPosts from "./pages/MyPosts"
import SubmitPost from "./pages/SubmitPost"
import { UserContext } from './UserContext';
import cookies from 'js-cookies';
import followService from './services/follow';

const App = () => {
  const [ user, setUser ] = useState("")
  const [ followers, setFollowers ] = useState([])
  
  useEffect(() => {
    if (cookies.hasItem("csrftoken") && localStorage.getItem("username")) {
      setUser(localStorage.getItem("username"));
    };
  }, []);

  useEffect(() => async () => {
    const res = followService.followers(localStorage.getItem("username"));
    if (user !== "") console.log(res)
  }, [user]);

  return (
    <UserContext.Provider value={{ user, setUser }}>
      <BrowserRouter>
        <Navbar />
        <Switch>
          <Route path="/friends">
            <Friends followers={followers} />
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
    </UserContext.Provider>
  )
};

export default App;
