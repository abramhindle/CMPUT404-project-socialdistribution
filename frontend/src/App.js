import { HashRouter as Router, Route } from "react-router-dom";
import React from "react";

import HomePage from "./pages/HomePage";
import LoginPage from "./pages/LoginPage";
import SignUpPage from "./pages/SignUpPage";
import PostPage from "./pages/PostPage";
import NotificationPage from "./pages/NotificationPage";
import FollowerPage from "./pages/FollowerPage";
import ProfilePage from "./pages/ProfilePage";
import ChangeProfilePage from "./pages/ChangeProfilePage";

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
      <Route path="/changeprofile" component={ChangeProfilePage} exact />
    </Router>
  );
}

export default App;
