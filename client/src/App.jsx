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
import jsCookies from 'js-cookies';

const App = () => {
  const [ user, setUser ] = useState();
  const [ followers, setFollowers ] = useState([])
  const [ inbox, setInbox ] = useState([])

  useEffect(() => {
    const setAuthor = async () => {
      const response = await authorService.getAuthor(localStorage.getItem("authorID"))
      setUser({
        username: localStorage.getItem("username"),
        author: {
          authorID: response.data.id.split('/').at(-1),
          displayName: response.data.displayName,
          profileImage: response.data.profileImage,
          host: null,
          github: response.data.github,
        },
      })
      return response;
    };
    if (localStorage.getItem("authorID") !== null && localStorage.getItem("username") !== null && jsCookies.hasItem("csrftoken")) {
      setAuthor();
    }
  }, []);

  useEffect(() => {
    if (user?.author?.authorID === undefined || user?.author?.authorID == null) return;
    const getInbox = async () => {
      const response = await authorService.getInbox(jsCookies.getItem("csrftoken"), user.author.authorID);
      setInbox(response.data.items)
      console.log(response);
    }
    getInbox();
  }
  , [user]);

  useEffect(() => {
    if (user?.author?.authorID === undefined || user?.author?.authorID == null) return;
    const getFollowers = async () => {
      const response = await authorService.getFollowers(user?.author?.authorID);
      setFollowers(response.data.items)
      console.log(response);
    }
    getFollowers();
  }
  , [user]);

  return (
    <UserContext.Provider value={{ user, setUser }}>
      <BrowserRouter>
        <Navbar />
        <Switch>
        {!user?.username ? (
          <>
            <Route path="/register">
              <Register />
            </Route>
            <Route path="/">
              <Login />
            </Route>
          </>
        ) : (
          <>
            <Route path="/friends">
              <Friends followers={followers} />
            </Route>
            <Route path="/myposts">
              <MyPosts />
            </Route>
            <Route path="/submit">
              <SubmitPost />
            </Route>
            <Route path="/profile">
              <Profile />
            </Route>
            <Route path="/" exact >
              <Home inbox={inbox} setInbox={setInbox} />
            </Route>
          </>
        )}
        </Switch>
      </BrowserRouter>
    </UserContext.Provider>
  )
};

export default App;
