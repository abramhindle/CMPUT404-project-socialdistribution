import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { PrivateRoute, SignInRoute } from "./utils/CustomRoute";
import SignIn from "./pages/Login/Signin";
import Friends from "./pages/Friends/friends";
import Followed from "./pages/Friends/followed";
import Followers from "./pages/Friends/followers";
import Request from "./pages/Friends/request";
import Posts from "./pages/Posts/new-post-page";
import Stream from "./pages/Stream";
import Profile from "./pages/Profile/profile";
import Realfriends from "./pages/Friends/realfriends";
import PostDetail from "./pages/Posts/post-detail";
import ImagePost from "./pages/Posts/image-post-page";

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
                <Stream filter="stream"/>
              </PrivateRoute>
            }>
              <Route path="inbox"
                element={
                  <PrivateRoute>
                    <Stream filter="inbox" />
                  </PrivateRoute>
                }>
                </Route>
              <Route path="foryou"/>
              <Route path="likes"/>
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
            }>
            <Route path="new"
              element={
                <PrivateRoute>
                  <Posts />
                </PrivateRoute>
              }/>
            <Route path="sent"/>
          </Route>
          <Route exact path="/posts/image"
            element={
              <PrivateRoute>
                <ImagePost />
              </PrivateRoute>
          }/>
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
