import "./App.css";

import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { PrivateRoute, SignInRoute } from "./utils/CustomRoute";
import SignIn from "./Signin";
import Friends from "./pages/Friends/friends"
import Posts from "./pages/Posts/posts";
import Main from "./pages/Main";

function App() {
  return (
    <div>
      <Router>
        <Routes>
          {/* Inbox */}
          <Route path="/"
            element={
              <PrivateRoute>
                <Main />
              </PrivateRoute>
            }>
              <Route path="foryou"/>
              <Route path="likes"/>
          </Route>
          {/* Friends */}
          <Route path="/friends"
            element={
              <PrivateRoute>
                <Friends />
              </PrivateRoute>
            }>
              <Route path="requests"/>
              <Route path="true"/>
              <Route path="followed"/>
              <Route path="follwers"/>
            </Route>
          {/* Posting */}
          <Route path="/posts"
            element={
              <PrivateRoute>
                <Posts />
              </PrivateRoute>
            }>
            <Route path="new"/>
            <Route path="sent"/>
          </Route>
          {/* Sign In */}
          <Route
            path="/signin"
            element={
              <SignInRoute>
                <SignIn />
              </SignInRoute>
            }
          />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
