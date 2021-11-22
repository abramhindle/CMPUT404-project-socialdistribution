import { HashRouter as Router, Route } from "react-router-dom";
import React from "react";

import HomePage from "./pages/HomePage";
import LoginPage from "./pages/LoginPage";
import SignUpPage from "./pages/SignUpPage";
import PostPage from "./pages/PostPage";
import NotificationPage from "./pages/NotificationPage";
import FollowerPage from "./pages/FollowerPage";
import ProfilePage from "./pages/ProfilePage";
import EditProfilePage from "./pages/EditProfilePage";
import SearchResultPage from "./pages/SearchResultPage";
import SearchUserPage from "./pages/SearchUserPage";


function App() {
  return (
    <Router>
      <Route path="/" component={HomePage} exact />
      <Route path="/login" component={LoginPage} exact />
      <Route path="/signup" component={SignUpPage} exact />
      <Route path="/post" component={PostPage} exact />
      <Route path="/notification" component={NotificationPage} exact />
      <Route path="/followers" component={FollowerPage} exact />
      <Route path="/profile" component={ProfilePage} exact />
      <Route path="/profile/:id" component={ProfilePage}></Route>
      <Route path="/editprofile" component={EditProfilePage} exact />
      <Route path="/searchresult/:id" component={SearchResultPage}></Route>
      <Route path="/searchuser/:id" component={SearchUserPage}></Route>
    </Router>
  );
}

export default App;
