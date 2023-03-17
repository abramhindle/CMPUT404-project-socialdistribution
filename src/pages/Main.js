import { useSelector, useDispatch } from "react-redux";
import { clearUser } from "../reducer/userSlice.js";
import { signOut_api } from "../api/user_api";
import Inbox from "./Inbox/inbox";

function Main(filter) {
  const user = useSelector((state) => state.user);
  const dispatch = useDispatch();

  const signOut = () => {
    dispatch(clearUser(user));
  };

  return (
    <div>
      Main! Welcome {user.displayName}
      <button onClick={() => signOut_api(signOut)}> Sign Out </button>
      <Inbox filter={filter}/>
    </div>
  );
}

export default Main;
