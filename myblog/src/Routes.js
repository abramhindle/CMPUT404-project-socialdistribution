import React from "react"
import { Route } from "react-router"
import User from "./User"
import UserSelf from "./UserSelf"
import Settings from "./Settings"
import Comments from "./Comment"
import FriendsList from "./FriendsList"
import FriendRequest from "./FriendRequest"
import PostInput from "./PostInput"
import PostEdit from "./PostEdit"
import Login from "./Login"
import Register from "./Register"
import SignUpRequestPage from "./SignUpRequestPage";
import NodesRequestPage from './NodesRequestPage';
import NodesPage from './NodesPage';
import AuthorPage from './AuthorPage';
import ProfilePage from './ProfilePage';
import AddNodesPage from './AddNodesPage';
import {reactLocalStorage} from 'reactjs-localstorage';

var urlpostid = reactLocalStorage.get("urlpostid");
var urlauthorid = reactLocalStorage.get("urlauthorid");

var urljoin = require('url-join');
var commentUrl = urljoin("/posts", String(urlpostid), "/comments");
var profileUrl = urljoin("/author", String(urlauthorid));
var friendsListUrl = urljoin("/author", String(urlauthorid), "/friends");
var friendsRequestUrl = urljoin("/author", String(urlauthorid), "/friendrequest");


const Routes = () => {
  return (
    <div>
      {/*author*/}
      <Route exact path="/" component={Login} />
      <Route path="/register" component={Register} />
      <Route path="/author/posts" component={User} />
      <Route exact path={profileUrl} component={UserSelf} />
      <Route path="/settings" component={Settings} />
      <Route path={commentUrl} component={Comments} /> 
      <Route path={friendsListUrl} component={FriendsList} />
      <Route path={friendsRequestUrl} component={FriendRequest} />
      <Route path="/postinput" component={PostInput} />
      <Route path="/postedit" component={PostEdit} />
      
      {/*admin*/}
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
