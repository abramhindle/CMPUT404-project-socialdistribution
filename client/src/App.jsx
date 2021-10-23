import './App.css';
import React, { useEffect, useState } from 'react';
import { Route, BrowserRouter, Switch } from 'react-router-dom';
import Navbar from "./components/Navbar"
import Home from "./pages/Home"
import Login from "./pages/Login"
import Register from "./pages/Register"
import Friends from "./pages/Friends"
import MyPosts from "./pages/MyPosts"
import Profile from './pages/Profile';
import SubmitPost from "./pages/SubmitPost"
import { UserContext } from './UserContext';
import authorService from './services/author';

const App = () => {
  const [user, setUser] = useState({
    username: null,
    author: {
      authorID: null,
      displayName: null,
      host: null,
      github: null,
      profileImage: null,
    },
  });

  const [ followers, setFollowers ] = useState([])

  useEffect(() => {
    const getFollowers = async () => {
      const response = await authorService.getFollowers(user.author.displayName);
      setFollowers(response.data.items)
      console.log(response);
    }
    if (user.id !== null) console.log(getFollowers())
  }
  , [user]);

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
          <Route path="/profile">
            <Profile />
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
