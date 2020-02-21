import React from "react"
import { Route } from "react-router"
import User from "./User"
import UserSelf from "./UserSelf"
import Settings from "./Settings"
import Comments from "./Comment"
import FriendsList from "./FriendsList"



const Routes = () => {
  return (
    <div>
      <Route exact path="/author/posts" component={User} />
      <Route path="/author/authorid" component={UserSelf} />
      <Route path="/Settings" component={Settings} />
      <Route path="/posts/postid/comments" component={Comments} />
      <Route path="/author/friends" component={FriendsList} />
    </div>
  )
}

export default Routes
