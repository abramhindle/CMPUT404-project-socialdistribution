import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { PrivateRoute, SignInRoute } from "./utils/CustomRoute";
import SignIn from "./pages/Login/Signin";
import SignUp from "./pages/Login/Signup";
import Friends from "./pages/Friends/friends";
import Followed from "./pages/Friends/followed";
import Followers from "./pages/Friends/followers";
import Request from "./pages/Friends/request";
import Posts from "./pages/Posts/new-post-page";
import Stream from "./pages/Stream";
import Inbox from "./pages/Inbox/inbox";
import Profile from "./pages/Profile/profile";
import Realfriends from "./pages/Friends/realfriends";
import PostDetail from "./pages/Posts/post-detail";
import ProfileEdit from "./pages/Profile/profile-edit";
import ImagePost from "./pages/Posts/image-post-page";

function App() {
  return (
    <div>
      <Router>
        <Routes>
          {/* Inbox */}
          <Route
            exact path="/"
            element={
              <PrivateRoute>
                <Stream/>
              </PrivateRoute>
            }/>
          <Route exact path="/inbox"
            element={
              <PrivateRoute>
                <Inbox/>
              </PrivateRoute>
            }/>
          {/* Friends */}
          <Route
            path="/friends"
            element={
              <PrivateRoute>
                <Friends />
              </PrivateRoute>
            }
          />
          <Route
            path="/friends/requests"
            element={
              <PrivateRoute>
                <Request />
              </PrivateRoute>
            }
          />
          <Route
            path="/friends/true"
            element={
              <PrivateRoute>
                <Realfriends />
              </PrivateRoute>
            }
          />
          <Route
            path="/friends/followed"
            element={
              <PrivateRoute>
                <Followed />
              </PrivateRoute>
            }
          />
          <Route
            path="/friends/followers"
            element={
              <PrivateRoute>
                <Followers />
              </PrivateRoute>
            }
          />
          {/* Posting */}
          <Route
            path="/posts"
            >
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
            exact
            path="user/:author_id"
            element={
              <PrivateRoute>
                <Profile />
              </PrivateRoute>
            }
          ></Route>
          <Route
            path="user/:author_id/edit"
            element={
              <PrivateRoute>
                <Posts />
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
          />
          <Route
            exact
            path="user/:author_id/post/:post_id/edit"
            element={
              <PrivateRoute>
                <Posts/>
              </PrivateRoute>
            }/>
          {/* Sign Up */}
          <Route
            path="/signup"
            element={
              <SignInRoute>
                <SignUp />
              </SignInRoute>
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
          <Route path="/*"  status={404}/>
        </Routes>
      </Router>
    </div>
  );
}

export default App;
