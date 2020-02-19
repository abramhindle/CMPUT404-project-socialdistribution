import React from "react"
import { Route } from "react-router"
import User from "./User"
import UserSelf from "./UserSelf"
import Settings from "./Settings"


const Routes = () => {
  return (
    <div>
      <Route exact path="/" component={User} />
      <Route path="/UserSelf" component={UserSelf} />
      <Route path="/Settings" component={Settings} />
    </div>
  )
}

export default Routes
