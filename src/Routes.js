import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { PrivateRoute, SignInRoute } from "./utils/CustomRoute";
import SignIn from "./pages/Login/Signin";
import Friends from "./pages/Friends/friends";
import Followed from "./pages/Friends/followed";
import Followers from "./pages/Friends/followers";
import Request from "./pages/Friends/request";
import Posts from "./pages/Posts/new-post-page";
import Main from "./pages/Main";
import Profile from "./pages/Profile/profile";
import Realfriends from "./pages/Friends/realfriends";

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
            }/>
              <Route path="/friends/requests"
                element={
                  <PrivateRoute>
                    <Request />
                  </PrivateRoute>
              }/>
              <Route path="/friends/true"
                element={
                  <PrivateRoute>
                    <Realfriends />
                  </PrivateRoute>
            }
              />
            <Route path="/friends/followed"
              element={
                <PrivateRoute>
                  <Followed />
                </PrivateRoute>
            }/>
              <Route path="/friends/followers"
              element={
                <PrivateRoute>
                  <Followers />
                </PrivateRoute>
            }/>
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
