import { Navigate } from "react-router-dom";
import { useSelector } from "react-redux";

export const PrivateRoute = ({ children }) => {
  const user = useSelector((state) => state.user);

  return user.isLogin ? children : <Navigate to="/signin" replace />;
};

export const SignInRoute = ({ children }) => {
  const user = useSelector((state) => state.user);

  return user.isLogin ? <Navigate to="/" replace /> : children;
};

export default { PrivateRoute, SignInRoute };
