import { Route, Navigate } from "react-router-dom";
import { useContext } from "react";
import AuthContext from "../Auth";

const PrivateRoute = ({ children, ...rest }) => {
  let { user } = useContext(AuthContext);
  if (!user) {
    // not logged in so redirect to login page with the return url
    return <Navigate to="/login" />;
  }

  // authorized so return child components
  return children;
  // return <Route {...rest}>{!user ? <Navigate to="/login" /> : children}</Route>;
};

export default PrivateRoute;
