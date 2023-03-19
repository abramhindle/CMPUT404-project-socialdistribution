import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { PrivateRoute, SignInRoute } from "./utils/CustomRoute";
import SignIn from "./pages/Login/Signin";
import Friends from "./pages/Friends/friends";
import Posts from "./pages/Posts/new-post-page";
import Main from "./pages/Main";
import Profile from "./pages/Profile/profile";
import PostDetail from "./pages/Posts/post-detail";

function App() {
  return (
    <div>
      <Router>
        <Routes>
          {/* Inbox */}
          <Route
            path="/"
            element={
              <PrivateRoute>
                <Main filter="feed" />
              </PrivateRoute>
            }
          >
            <Route
              path="feed"
              element={
                <PrivateRoute>
                  <Main filter="feed" />
                </PrivateRoute>
              }
            ></Route>
            <Route path="foryou" />
            <Route path="likes" />
          </Route>
          {/* Friends */}
          <Route
            path="/friends"
            element={
              <PrivateRoute>
                <Friends />
              </PrivateRoute>
            }
          >
            <Route path="requests" />
            <Route path="true" />
            <Route path="followed" />
            <Route path="followers" />
          </Route>
          {/* Posting */}
          <Route
            path="/posts"
            element={
              <PrivateRoute>
                <Posts />
              </PrivateRoute>
            }
          >
            <Route path="new" />
            <Route path="sent" />
          </Route>
          <Route
            path="user/:author_id"
            element={
              <PrivateRoute>
                <Profile />
              </PrivateRoute>
            }
          ></Route>
          <Route
            path="user/:author_id/post/:post_id"
            element={
              <PrivateRoute>
                <PostDetail />
              </PrivateRoute>
            }
          ></Route>
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
