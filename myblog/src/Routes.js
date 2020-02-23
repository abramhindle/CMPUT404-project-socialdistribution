import React from "react"
import { Route } from "react-router"
import SignUpRequestPage from "./SignUpRequestPage";
import NodesRequestPage from './NodesRequestPage';
import NodesPage from './NodesPage';
import AuthorPage from './AuthorPage';
import ProfilePage from './ProfilePage';
import AddNodesPage from './AddNodesPage';

const Routes = () => {
  return (
    <div>
      <Route exact path="/" component={SignUpRequestPage} />
      <Route path="/nodes-request" component={NodesRequestPage} />
      <Route path="/my-nodes" component={NodesPage} />
      <Route path="/authors" component={AuthorPage} />
      <Route path="/profile" component={ProfilePage} />
      <Route path="/add-nodes" component={AddNodesPage} />
    </div>
  )
}

export default Routes