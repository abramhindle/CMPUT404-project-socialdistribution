import React from "react"
import { Route } from "react-router"
import User from "./User"
import UserSelf from "./UserSelf"
import Settings from "./Settings"
import Comments from "./Comment"
import FriendsList from "./FriendsList"
import PostList from "./Jsontest"
import PostInput from "./PostInput"

import Login from "./Login"
import Register from "./Register"

import SignUpRequestPage from "./SignUpRequestPage";
import NodesRequestPage from './NodesRequestPage';
import NodesPage from './NodesPage';
import AuthorPage from './AuthorPage';
import ProfilePage from './ProfilePage';
import AddNodesPage from './AddNodesPage';


const Routes = () => {
  return (
    <div>
      <Route exact path="/" component={Login} />
      <Route path="/register" component={Register} />
      <Route path="/author/posts" component={User} />
      <Route path="/author/authorid" component={UserSelf} />
      <Route path="/Settings" component={Settings} />
      <Route path="/posts/postid/comments" component={Comments} />
      <Route path="/author/friends" component={FriendsList} />
      <Route path="/test" component={PostList} />
      <Route path="/postinput" component={PostInput} />

      <Route path="/sign-up-request" component={SignUpRequestPage} />
      <Route path="/nodes-request" component={NodesRequestPage} />
      <Route path="/my-nodes" component={NodesPage} />
      <Route path="/authors" component={AuthorPage} />
      <Route path="/profile" component={ProfilePage} />
      <Route path="/add-nodes" component={AddNodesPage} />
    </div>
  )
}

export default Routes
