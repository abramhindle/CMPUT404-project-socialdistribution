import logout_api from "./logout_api";
import { useSelector, useDispatch } from "react-redux";
import { clearUser } from "./reducer/userSlice.js";

function Main() {
  const user = useSelector((state) => state.user);
  const dispatch = useDispatch();

  const signOut = () => {
    dispatch(clearUser(user));
  };

  return (
    <div>
      Main! Welcome {user.displayName}
      <button onClick={() => logout_api(signOut)}> Sign Out </button>
    </div>
  );
}

export default Main;
