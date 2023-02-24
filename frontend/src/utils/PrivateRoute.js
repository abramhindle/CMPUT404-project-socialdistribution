import { Navigate, useLocation } from "react-router-dom";
import { useSelector } from "react-redux";

const PrivateRoute = ({ children }) => {
  const user = useSelector((state) => state.user);
  console.log(user.isLogin);

  return user.isLogin ? children : <Navigate to="/login" replace />;
};

export default PrivateRoute;
